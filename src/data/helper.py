
def apply_query_et_sort(query, q, sort):
    if not q and not sort:
        query.order('created_at', desc=True)
  
    if q:
        query = query.or_(f"provider.ilike.%{q}%,type.ilike.%{q}%")

    if sort:
        if sort == "az":
            query = query.order("provider", desc=False)  # A-Z
        elif sort == "za":
            query = query.order("provider", desc=True)  # Z-A
        elif sort == "new":
            query = query.order("created_at", desc=True)  # Newest First
        elif sort == "old":
            query = query.order("created_at", desc=False)  # Oldest First
        elif sort == "short":
            query = query.order("duration", desc=False)  # Shortest Duration First
        elif sort == "long":
            query = query.order("duration", desc=True)  # Longest Duration First
    return query
