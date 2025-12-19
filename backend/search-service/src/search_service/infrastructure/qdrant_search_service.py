import logging
from typing import List, Optional

from qdrant_client import QdrantClient as QdrantClientSDK
from qdrant_client.models import Filter, FieldCondition, MatchValue

from search_service.config import config
from search_service.core.dto.search_result_dto import SearchResultItemDTO
from search_service.core.interface.service.vector_search_service import VectorSearchService

logger = logging.getLogger(__name__)


class QdrantSearchService(VectorSearchService):
    def __init__(self):
        logger.info(
            "Initializing Qdrant search service",
            extra={
                "host": config.qdrant.host,
                "port": config.qdrant.port,
                "collection": config.qdrant.collection_name,
            }
        )
        self.client: QdrantClientSDK = QdrantClientSDK(
            host=config.qdrant.host,
            port=config.qdrant.port,
        )
        self.collection_name = config.qdrant.collection_name

    async def search_by_vector(
        self,
        vector: List[float],
        limit: int = 20,
        user_id: Optional[str] = None,
        query_text: Optional[str] = None,
    ) -> List[SearchResultItemDTO]:
        """
        Search for similar vectors in Qdrant.
        
        Args:
            vector: Query vector
            limit: Maximum number of results to return
            user_id: Optional user ID to filter results
            
        Returns:
            List of search result items sorted by similarity
        """
        try:
            import math
            vector_norm = math.sqrt(sum(x * x for x in vector))
            norm_check = "normalized" if abs(vector_norm - 1.0) < 0.01 else "NOT_NORMALIZED"
            logger.info(
                f"Searching vectors in Qdrant: vector_dimension={len(vector)}, vector_norm={vector_norm:.6f}, norm_check={norm_check}, limit={limit}, user_id={user_id}",
                extra={
                    "limit": limit,
                    "user_id": user_id,
                    "vector_dimension": len(vector),
                    "vector_norm": vector_norm,
                    "vector_norm_check": norm_check,
                }
            )

            query_filter = None
            if user_id:
                query_filter = Filter(
                    must=[
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value=user_id)
                        )
                    ]
                )

            search_result = self.client.query_points(
                collection_name=self.collection_name,
                query=vector,
                query_filter=query_filter,
                limit=limit,
            )
            
            if search_result.points:
                first_scores = [hit.score for hit in search_result.points[:3]]
                logger.info(
                    f"Qdrant search results - first few scores: {first_scores}, range: {min(first_scores):.4f} - {max(first_scores):.4f}",
                    extra={
                        "first_scores": first_scores,
                        "score_range": f"{min(first_scores):.4f} - {max(first_scores):.4f}",
                        "note": "Qdrant COSINE distance returns similarity directly (range: -1 to 1, where 1 = perfect match)",
                    }
                )

            results = []
            min_similarity = config.qdrant.min_similarity_threshold
            
            for hit in search_result.points:
                similarity = hit.score
                
                if similarity > 1.0 or similarity < -1.0:
                    logger.warning(
                        f"Qdrant score out of expected range [-1, 1]: {similarity}",
                        extra={
                            "score": similarity,
                            "object_name": hit.payload.get("object_name", ""),
                        }
                    )
                    similarity = max(-1.0, min(1.0, similarity))
                
                logger.info(
                    f"Processing search result: similarity={similarity:.6f}, object_name={hit.payload.get('object_name', '')}",
                    extra={
                        "object_name": hit.payload.get("object_name", ""),
                        "similarity": similarity,
                        "image_filename": hit.payload.get("image_filename", ""),
                    }
                )
                
                if similarity < min_similarity:
                    logger.warning(
                        f"FILTERED: similarity {similarity:.4f} below threshold {min_similarity:.4f}",
                        extra={
                        "object_name": hit.payload.get("object_name", ""),
                        "similarity": similarity,
                        "threshold": min_similarity,
                        }
                    )
                    continue
                
                results.append(
                    SearchResultItemDTO(
                        object_name=hit.payload.get("object_name", ""),
                        image_filename=hit.payload.get("image_filename", ""),
                        user_id=hit.payload.get("user_id", ""),
                        score=similarity,
                        point_id=str(hit.id),
                    )
                )
            
            results.sort(key=lambda x: x.score, reverse=True)
            
            if query_text:
                query_lower = query_text.lower()
                filtered_relevant = []
                for hit in search_result.points:
                    object_name = hit.payload.get("object_name", "").lower()
                    similarity = hit.score
                    query_keywords = [kw for kw in query_lower.split() if len(kw) > 3]
                    if any(keyword in object_name for keyword in query_keywords):
                        if similarity < min_similarity:
                            filtered_relevant.append({
                                "object_name": hit.payload.get("object_name", ""),
                                "similarity": similarity,
                            })
                
                if filtered_relevant:
                    logger.warning(
                        f"Relevant images filtered out due to low similarity!",
                        extra={
                            "query": query_text,
                            "filtered_count": len(filtered_relevant),
                            "min_threshold": min_similarity,
                            "filtered_images": filtered_relevant,
                        }
                    )
            
            if results:
                scores = [r.score for r in results]
                top_similarities = []
                for i, hit in enumerate(search_result.points[:min(5, len(search_result.points))]):
                    top_similarities.append({
                        "object_name": hit.payload.get("object_name", ""),
                        "similarity": hit.score,
                    })
                
                import json
                logger.info(
                    f"Search completed: results_count={len(results)}, similarity_range={min(scores):.4f}-{max(scores):.4f}, avg_similarity={sum(scores) / len(scores):.4f}, top_similarity={max(scores):.4f}, min_threshold={min_similarity}, top_similarities_sample={json.dumps(top_similarities)}",
                    extra={
                        "results_count": len(results),
                        "user_id": user_id,
                        "similarity_range": f"{min(scores):.4f} - {max(scores):.4f}",
                        "avg_similarity": f"{sum(scores) / len(scores):.4f}",
                        "top_similarity": f"{max(scores):.4f}",
                        "min_threshold": min_similarity,
                        "top_similarities_sample": top_similarities,
                    }
                )
            else:
                logger.info(
                    "Search completed with no results",
                    extra={
                        "user_id": user_id,
                        "min_threshold": min_similarity,
                    }
                )

            return results

        except Exception as e:
            logger.error(
                "Error searching vectors in Qdrant",
                extra={"error": str(e), "user_id": user_id},
                exc_info=True,
            )
            raise


qdrant_search_service = QdrantSearchService()

