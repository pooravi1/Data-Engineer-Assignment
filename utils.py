def safe_get_text(item, selector, class_name=None, default="None", index=None):
    """Safely get the text of an element, returning a default value if not found."""
    try:
        if index is not None:
            return item.find_all(selector, class_=class_name)[index].get_text(strip=True)
        else:
            return item.find(selector, class_=class_name).get_text(strip=True)
    except (AttributeError, IndexError):
        return default
