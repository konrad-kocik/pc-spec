def reorder_dict(dict_to_reorder, key_to_move, new_item_id, shift):
    value_to_move = dict_to_reorder[key_to_move]
    reordered_dict = {}

    for item_id, item in enumerate(dict_to_reorder.items()):
        key, value = item

        if key != key_to_move and shift > 0:
            reordered_dict[key] = value

        if item_id == new_item_id:
            reordered_dict[key_to_move] = value_to_move

        if key != key_to_move and shift < 0:
            reordered_dict[key] = value

    return reordered_dict
