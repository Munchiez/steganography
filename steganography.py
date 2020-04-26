import cv2

choice = input("Encode or Decode: ")


def encode():
    image_name = input("Image name: ")
    print("Five dashes indicate end of message")
    file_or_type = input("1 - type it out\n2 - text file")
    if file_or_type == "1":
        text = input("Text: ")
    else:
        file_name = input("File name: ")
        f = open(file_name, 'r')
        text = f.readlines()
        text = ''.join(text)
        f.close()
    output_name = input("Output name: ")

    binary_list = []
    for char in text:
        binary_value = str(bin(ord(char))).replace('0b', '')
        if len(binary_value) < 8:
            num_of_zeroes = 8 - len(str(binary_value))
            binary_value = f"{'0' * num_of_zeroes}{binary_value}"
        binary_list.append(str(binary_value))
    binary_combined_perm = ''.join(binary_list)
    binary_combined = binary_combined_perm

    image = cv2.imread(image_name)

    for row_index, row in enumerate(image):
        for pixel_index, pixel in enumerate(row):
            for rgb_index, rgb in enumerate(pixel):
                if len(binary_combined) < 1:
                    binary_combined = binary_combined_perm
                binary = str(bin(rgb)).replace("0b", "")
                if len(binary) < 8:
                    zeroes = 8 - len(binary)
                    binary = f"{'0' * zeroes}{binary}"
                goal_value = binary_combined[:2]
                actual_value = binary[-2:]
                if goal_value == actual_value:
                    pass
                else:
                    binary = binary[:-2]
                    binary += goal_value
                    new_rgb = int(binary, 2)
                    image[row_index, pixel_index, rgb_index] = new_rgb
                binary_combined = binary_combined[2:]

    cv2.imwrite(output_name, image)


def decode():
    file_name = input("File name: ")
    image = cv2.imread(file_name)

    binary_total_string = ""
    for row_index, row in enumerate(image):
        for pixel_index, pixel in enumerate(row):
            for rgb_index, rgb in enumerate(pixel):
                binary = str(bin(rgb)).replace('0b', '')
                if len(binary) < 8:
                    num_of_zeroes = 8 - len(binary)
                    binary = f"{'0' * num_of_zeroes}{binary}"
                wanted_values = binary[-2:]
                binary_total_string += wanted_values

    separate_binary_values = []
    temp_bin_str = ""
    index_of_bin = 0
    for num in binary_total_string:
        if index_of_bin == 8:
            separate_binary_values.append(temp_bin_str)
            index_of_bin = 0
            temp_bin_str = ""
        temp_bin_str += num
        index_of_bin += 1

    output_message = ""
    for num in separate_binary_values:
        character = chr(int(num, 2))
        output_message += character
    print(output_message)

    dashes = output_message.index('?????')
    output_message = output_message[:dashes]
    print(output_message)


if choice.lower() == "encode":
    encode()
elif choice.lower() == "decode":
    decode()
