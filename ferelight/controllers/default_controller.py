import psycopg2
import torch
from flask import current_app
from pgvector.psycopg2 import register_vector

from ferelight.controllers import tokenizer, model
from ferelight.models import Scoredsegment
from ferelight.models.multimediaobject import Multimediaobject  # noqa: E501
from ferelight.models.multimediasegment import Multimediasegment  # noqa: E501
from ferelight.models.objectinfos_post_request import ObjectinfosPostRequest  # noqa: E501
from ferelight.models.query_post_request import QueryPostRequest  # noqa: E501
from ferelight.models.scoredsegment import Scoredsegment  # noqa: E501
from ferelight.models.segmentbytime_post200_response import SegmentbytimePost200Response  # noqa: E501
from ferelight.models.segmentinfos_post_request import SegmentinfosPostRequest  # noqa: E501
from ferelight import util


def get_connection(database):
    return psycopg2.connect(dbname=database, user=current_app.config['DBUSER'],
                            password=current_app.config['DBPASSWORD'], host=current_app.config['DBHOST'],
                            port=current_app.config['DBPORT'])


def objectinfo_database_objectid_get(database, objectid):  # noqa: E501
    """Get the information of an object.

     # noqa: E501

    :param database: The name of the database to query for the object.
    :type database: str
    :param objectid: The unique identifier of the object.
    :type objectid: str

    :rtype: Union[Multimediaobject, Tuple[Multimediaobject, int], Tuple[Multimediaobject, int, Dict[str, str]]
    """
    with get_connection(database) as conn:
        cur = conn.cursor()
        cur.execute(f"""SELECT objectid, mediatype, name, path FROM cineast_multimediaobject WHERE objectid = %s""",
                    (objectid,))
        (objectid, mediatype, name, path) = cur.fetchone()
        return Multimediaobject(objectid=objectid, mediatype=mediatype, name=name, path=path)


def objectinfos_post(body):  # noqa: E501
    """Get the information of multiple objects.

     # noqa: E501

    :param objectinfos_post_request:
    :type objectinfos_post_request: dict | bytes

    :rtype: Union[List[Multimediaobject], Tuple[List[Multimediaobject], int], Tuple[List[Multimediaobject], int, Dict[str, str]]
    """
    with get_connection(body['database']) as conn:
        cur = conn.cursor()
        cur.execute(
            f"""SELECT objectid, mediatype, name, path FROM cineast_multimediaobject WHERE objectid = ANY(%s)""",
            (body['objectids'],))
        results = cur.fetchall()

    object_infos = [Multimediaobject(objectid=objectid, mediatype=mediatype, name=name, path=path) for
                    (objectid, mediatype, name, path) in results]

    return object_infos


def objectsegments_database_objectid_get(database, objectid):  # noqa: E501
    """Get the segments of an object.

     # noqa: E501

    :param database: The name of the database to query for the object.
    :type database: str
    :param objectid: The unique identifier of the object.
    :type objectid: str

    :rtype: Union[List[Multimediasegment], Tuple[List[Multimediasegment], int], Tuple[List[Multimediasegment], int, Dict[str, str]]
    """
    with get_connection(database) as conn:
        cur = conn.cursor()
        cur.execute(
            f"""
                SELECT segmentid, objectid, segmentnumber, segmentstart, segmentend, segmentstartabs, segmentendabs  
                FROM cineast_segment WHERE objectid = %s""",
            (objectid,))
        results = cur.fetchall()

    segmentinfos = [Multimediasegment(segmentid=segmentid, objectid=objectid, segmentnumber=segmentnumber,
                                      segmentstart=segmentstart, segmentend=segmentend, segmentstartabs=segmentstartabs,
                                      segmentendabs=segmentendabs) for
                    (segmentid, objectid, segmentnumber, segmentstart, segmentend, segmentstartabs, segmentendabs) in
                    results]

    return segmentinfos


def query_post(body):  # noqa: E501
    """Query the FERElight engine.

     # noqa: E501

    :param query_post_request:
    :type query_post_request: dict | bytes

    :rtype: Union[List[Scoredsegment], Tuple[List[Scoredsegment], int], Tuple[List[Scoredsegment], int, Dict[str, str]]
    """
    limit = f'LIMIT {body["limit"]}' if 'limit' in body else ''

    similarity_vector = []
    if 'similaritytext' in body:
        text = tokenizer(body['similaritytext'])
        with torch.no_grad():
            text_features = model.encode_text(text)
            text_features /= text_features.norm(dim=-1, keepdim=True)
            similarity_vector = text_features.cpu().numpy().flatten()

    with get_connection(body['database']) as conn:
        cur = conn.cursor()
        cur.execute('CREATE EXTENSION IF NOT EXISTS vector')
        register_vector(conn)
        # Set index parameter to allow for correct number of results
        if 'limit' in body:
            cur.execute('SET hnsw.ef_search = %s', (body['limit'],))
        if 'ocrtext' in body and not 'similaritytext' in body:
            cur.execute(
                f"""
                    SELECT id, 0 AS distance
                    FROM features_ocr WHERE feature @@ plainto_tsquery(%s)
                    {limit}
                """,
                (body['ocrtext'],))
        elif 'similaritytext' in body and not 'ocrtext' in body:
            # Get cosine similarity as score
            cur.execute(
                f"""
                    SELECT id, feature <=> %s AS distance
                    FROM features_openclip
                    ORDER BY distance
                    {limit}
                """,
                (similarity_vector,))
        elif 'ocrtext' in body and 'similaritytext' in body:
            cur.execute(
                f"""
                    SELECT id, feature <=> %s AS distance
                    FROM features_openclip
                    WHERE id IN (
                        SELECT id
                        FROM features_ocr
                        WHERE feature @@ plainto_tsquery(%s)
                    )
                    ORDER BY distance
                    {limit}
                """,
                (similarity_vector, body['ocrtext'])
            )

        results = cur.fetchall()
        scored_segments = [Scoredsegment(segmentid=segmentid, score=1 - distance) for (segmentid, distance) in results]
        return scored_segments


def segmentinfo_database_segmentid_get(database, segmentid):  # noqa: E501
    """Get the information of a segment.

     # noqa: E501

    :param database: The name of the database to query for the segment.
    :type database: str
    :param segmentid: The unique identifier of the segment.
    :type segmentid: str

    :rtype: Union[Multimediasegment, Tuple[Multimediasegment, int], Tuple[Multimediasegment, int, Dict[str, str]]
    """
    with get_connection(database) as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT segmentid, objectid, segmentnumber, segmentstart, segmentend, segmentstartabs, segmentendabs 
            FROM cineast_segment WHERE segmentid = %s
        """,
                    (segmentid,))
        (segmentid, objectid, segmentnumber, segmentstart, segmentend, segmentstartabs, segmentendabs) = cur.fetchone()
        return Multimediasegment(segmentid=segmentid, objectid=objectid, segmentnumber=segmentnumber,
                                 segmentstart=segmentstart, segmentend=segmentend, segmentstartabs=segmentstartabs,
                                 segmentendabs=segmentendabs)


def segmentinfos_post(body):  # noqa: E501
    """Get the information of multiple segments.

     # noqa: E501

    :param segmentinfos_post_request:
    :type segmentinfos_post_request: dict | bytes

    :rtype: Union[List[Multimediasegment], Tuple[List[Multimediasegment], int], Tuple[List[Multimediasegment], int, Dict[str, str]]
    """
    with get_connection(body['database']) as conn:
        cur = conn.cursor()
        cur.execute(
            f"""
                SELECT segmentid, objectid, segmentnumber, segmentstart, segmentend, segmentstartabs, segmentendabs  
                FROM cineast_segment WHERE segmentid = ANY(%s)""",
            (body['segmentids'],))
        results = cur.fetchall()

    segment_infos = [Multimediasegment(segmentid=segmentid, objectid=objectid, segmentnumber=segmentnumber,
                                       segmentstart=segmentstart, segmentend=segmentend,
                                       segmentstartabs=segmentstartabs,
                                       segmentendabs=segmentendabs) for
                     (segmentid, objectid, segmentnumber, segmentstart, segmentend, segmentstartabs, segmentendabs) in
                     results]

    return segment_infos


def querybyexample_post(body):  # noqa: E501
    """Get the nearest neighbors of a segment.

     # noqa: E501

    :param querybyexample_post_request:
    :type querybyexample_post_request: dict | bytes

    :rtype: Union[List[Scoredsegment], Tuple[List[Scoredsegment], int], Tuple[List[Scoredsegment], int, Dict[str, str]]
    """
    with get_connection(body['database']) as conn:
        cur = conn.cursor()
        cur.execute('CREATE EXTENSION IF NOT EXISTS vector')
        register_vector(conn)

        limit = f'LIMIT {body["limit"]}' if 'limit' in body else ''

        if 'limit' in body:
            cur.execute('SET hnsw.ef_search = %s', (body['limit'],))

        cur.execute(
            f"""
            WITH query_feature AS (
                SELECT feature 
                FROM features_openclip 
                WHERE id = %s 
                LIMIT 1
            )
            SELECT 
                id, 
                (feature <=> (SELECT feature FROM query_feature)) AS distance
            FROM features_openclip
            WHERE id != %s
            ORDER BY distance
            {limit}
            """,
            (body['segmentid'], body['segmentid'])
        )

        results = cur.fetchall()
        scored_segments = [Scoredsegment(segmentid=segmentid, score=1 - distance) for (segmentid, distance) in results]
    return scored_segments


def segmentbytime_post(body):  # noqa: E501
    """Get the segment ID for a given timestamp and object.

     # noqa: E501

    :param segmentbytime_post_request:
    :type segmentbytime_post_request: dict | bytes

    :rtype: Union[SegmentbytimePost200Response, Tuple[SegmentbytimePost200Response, int], Tuple[SegmentbytimePost200Response, int, Dict[str, str]]
    """
    with get_connection(body['database']) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT segmentid 
            FROM cineast_segment 
            WHERE objectid = %s 
            AND %s BETWEEN segmentstartabs AND segmentendabs;
            """,
            (body['objectid'], body['timestamp'])
        )

        result = cur.fetchone()

    if result:
        return SegmentbytimePost200Response(segmentid=result[0])

    return {}, 404  # No matching segment found
