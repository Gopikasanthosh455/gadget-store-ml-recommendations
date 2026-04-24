import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from AdminApp.models import productDB
from WebApp.models import productViewEvent


def get_recommended_products(product_id, limit=4):
    interactions = productViewEvent.objects.select_related("product").all()
    if interactions.count() < 2:
        return list(
            productDB.objects.exclude(id=product_id).order_by("?")[:limit]
        )

    rows = []
    for interaction in interactions:
        viewer_id = interaction.Username or interaction.session_key
        if viewer_id:
            rows.append(
                {
                    "viewer_id": viewer_id,
                    "product_id": interaction.product_id,
                    "view_strength": 1,
                }
            )

    if len(rows) < 2:
        return list(
            productDB.objects.exclude(id=product_id).order_by("?")[:limit]
        )

    frame = pd.DataFrame(rows)
    interaction_matrix = frame.pivot_table(
        index="viewer_id",
        columns="product_id",
        values="view_strength",
        aggfunc="sum",
        fill_value=0,
    )

    if product_id not in interaction_matrix.columns:
        return list(
            productDB.objects.exclude(id=product_id).order_by("?")[:limit]
        )

    similarity_matrix = cosine_similarity(interaction_matrix.T)
    similarity_frame = pd.DataFrame(
        similarity_matrix,
        index=interaction_matrix.columns,
        columns=interaction_matrix.columns,
    )

    similar_products = (
        similarity_frame[product_id]
        .drop(labels=[product_id], errors="ignore")
        .sort_values(ascending=False)
    )
    similar_ids = [int(item_id) for item_id in similar_products.head(limit * 2).index.tolist()]

    recommended_by_similarity = list(productDB.objects.filter(id__in=similar_ids))
    ordered_recommendations = sorted(
        recommended_by_similarity,
        key=lambda product: similar_ids.index(product.id),
    )

    if len(ordered_recommendations) >= limit:
        return ordered_recommendations[:limit]

    fallback_products = list(
        productDB.objects.exclude(id__in=[product_id, *similar_ids]).order_by("?")[
            : max(limit - len(ordered_recommendations), 0)
        ]
    )
    return ordered_recommendations + fallback_products
