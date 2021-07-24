arabic_letters = ['أ', 'ة', 'إ', 'ؤ', 'آ', 'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز',
                  'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي', 'ئ', 'ئ', 'ء', 'ى']
arabic_diacs = ["َ", "ً", "ِ", "ٍ", "ُ", "ٌ", "ْ", "َّ", "ِّ", "ُّ", "ّ"]


def _filter_funtion(variable):
    return (variable not in arabic_diacs)


def _remove_diac(example, isDataset=True):
    if isDataset:
        example = example['text']

    example_arr = [char for char in example]
    final_arr = filter(_filter_funtion, example_arr)
    final_text = ''.join(final_arr)
    return {'text': final_text, 'diacritized': example}


def _create_mask_arr(sentence):
    masks_arr = []
    s_arr = [char for char in sentence]
    for i in range(1, len(s_arr)):
        if s_arr[i] in arabic_letters:
            masks_arr.append(''.join([*s_arr[0:i], '<mask>', *s_arr[i:]]))
    masks_arr.append(''.join([*s_arr, '<mask>']))
    return masks_arr


def _fill_mask_arr(fill_mask, arr):
    fills = []
    for i in arr:
        if fill_mask(i)[0]['token_str'] == ' ':
            fills.append(fill_mask(i)[1])
        else:
            fills.append(fill_mask(i)[0])
    return fills


def _create_seq_from_fills(fills):
    seq_of_diac = [i['token_str'] for i in fills]
    return seq_of_diac


def _fix_fills(diacritized_sentence, fill_mask):
    output_arr = [char for char in diacritized_sentence]
    o_mask_arr = []
    for i in range(len(output_arr)):
        if diacritized_sentence[i] in arabic_diacs:
            o_mask_arr.append(
                ''.join([*output_arr[0:i], '<mask>', *output_arr[i+1:]]))

    fills = []
    for i in o_mask_arr:
        if fill_mask(i)[0]['token_str'] == ' ':
            fills.append(fill_mask(i)[1])
            # fills.append({'token_str': ''})
        else:
            fills.append(fill_mask(i)[0])

    return fills


def _mix_letters_and_diacs(sentence, seq_of_diac):
    diac_iterator = 0
    output = ""

    for i in range(len(sentence)):
        if sentence[i] in arabic_letters:
            output += sentence[i]
            output += seq_of_diac[diac_iterator]
            diac_iterator += 1
        elif sentence[i] == ' ':
            output += " "

    return output


def diacritize(sentence, fill_mask, passes=1, isDataset=False):

    removed_diac_sentence = _remove_diac(sentence, isDataset)['text']
    mask_array = _create_mask_arr(removed_diac_sentence)
    fills = _fill_mask_arr(fill_mask, mask_array)
    seq_of_diac = _create_seq_from_fills(fills)
    output = _mix_letters_and_diacs(sentence, seq_of_diac)

    if passes > 1:
        for i in range(1, passes):
            fixed_fills = _fix_fills(output, fill_mask)
            seq_of_diac = _create_seq_from_fills(fixed_fills)
            output = _mix_letters_and_diacs(sentence, seq_of_diac)

    return output
