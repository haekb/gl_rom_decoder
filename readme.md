# ROM Decoder

Decodes Gauntlet Legends Dreamcast `DISK.ROM` and `SIZES.ROM` files. 

## Usage
Place both your `DISK.ROM` and `SIZES.ROM` files into the same directory as the scripts, and run `rom_decoder.py`. Afterwords you should see a `out/` folder. You will also see a `not_in_archive.txt`, which just contains a list of files that weren't packed into the archive or are just missing. (This is normal.)

## Structure
`SIZES.ROM` and `DISK.ROM` are fairly simple formats. `SIZES.ROM` contains a total file count, a list of file sizes, offsets (for `DISK.ROM`) and file paths stored as such:
```
struct Header{
    uint Count;
}
struct Entry {
    uint Size;
    uint Offset;
    // Relative to the end of entries
    short PathOffsets[4];
};
```

You then need to loop per each PathOffsets, offset from the end of your Entry list and read the null terminated string. If you reach -1 (or 0xFFFF) in your PathOffsets list then break from the loop.

Once you've read `SIZES.ROM`, simply load up `DISK.ROM`. Loop through each Entry, seeking (from the start of the file) to the Offset, and reading until you hit Size.

## Credits
Some helper functions are from [io_scene_abc](https://github.com/cmbasnett/io_scene_abc), at least for the time being!
Research and development by [Haekb (HeyThereCoffeee)](https://github.com/haekb)