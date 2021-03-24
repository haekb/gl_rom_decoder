import os
from pathlib import Path
from io_utils import unpack, read_string

def read_sizes(f):
    count = unpack('I', f)[0]
    entries = []

    for _i in range(count):
        entries.append({
            'size': unpack('I', f)[0],
            'offset': unpack('I', f)[0],
            'path_indexes': unpack('4H', f),
            'path': '',
        })
    # End For

    path_offset_start = f.tell()

    # Okay we're through the entry list, we can now grab the paths!
    for i in range(count):
        entry = entries[i]
        path_strings = []
        
        for path_index in entry['path_indexes']:
            if path_index == 65535:
                break
            f.seek(path_offset_start, 0)
            f.seek(path_index, 1)
            path_strings.append(read_string(f))
        # End For

        path = '/'.join(path_strings)
        entries[i]['path'] = path
    # End For

    return entries
# End Def

def read_disk(entries, root_out, f):
    # We don't actually need to read this data, but I already wrote it...so here it is!    
    # # Header
    # version = unpack('I', f)[0]
    # audio_file_count = unpack('I', f)[0]
    # unk_data_pointer = unpack('I', f)[0]
    # unk_data_pointer2 = unpack('I', f)[0]
    # unk_data_pointer3 = unpack('I', f)[0]
    # audio_data_pointer = unpack('I', f)[0]
    
    # # Audio Files
    # f.seek(audio_data_pointer, 0)

    # audio_file_entries = []
    # for _i in range(audio_file_count):
    #     audio_file_entries.append({
    #         'name': f.read(16).decode('ascii'),
    #         'index':  unpack('I', f)[0],
    #         'unk1': unpack('f', f)[0],
    #         'unk2': unpack('I', f)[0],
    #     })
    # # End For

    not_used_list = []

    for entry in entries:
        # These files aren't actually in the archive!
        if entry['offset'] == 4294967295: # -1 Signed
            not_used_list.append(entry)
            continue
        # End If

        buffer = ''
        out = entry['path']

        # Head to the data!
        f.seek(entry['offset'], 0)
        buffer = f.read(entry['size'])

        # Create our path
        out_path = Path(os.path.dirname("%s/%s" % (root_out, out)))
        out_path.mkdir(parents=True, exist_ok=True)

        # Write it all out at once!
        f_file = open("%s/%s" % (root_out, out), 'wb')
        f_file.write(buffer)
        f_file.close()
    # End For

    f_not_used = open("./not_in_archive.txt", 'w')

    for entry in not_used_list:
        f_not_used.write("%s\n" % entry['path'])
    # End For

    f_not_used.close()

# End Def

def main():
    print("ROM Decoder by @HeyThereCoffeee")
    print("For Gauntlet Legends (Dreamcast)")

    root_out = './out/'

    # Create our root output directory
    path = Path(root_out)
    path.mkdir(parents=True, exist_ok=True)

    print("Opening DISK.ROM and SIZES.ROM...")
    f_disk = open('./DISK.ROM', 'rb')
    f_size = open('./SIZES.ROM', 'rb')

    print("Reading SIZES.ROM")
    entries = read_sizes(f_size)
    print("Finished reading SIZES.ROM")
    f_size.close()

    print("Reading DISK.ROM and extracting files!")
    read_disk(entries, root_out, f_disk)
    # Close them files!
    f_disk.close()

    print("Finished extracting files!")

    print("All done!")

# End Def


main()