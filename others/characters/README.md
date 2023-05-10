# General

## Unicode
  * Standard for representing all possible characters in a uniform way - also provides high storage efficiency and is computationally efficient and consistent.

### UTF-8
  * 8-bit/1-byte units - 4 available, ie, 1-byte, 2-byte, 3-byte, 4-byte
  * Can encode all valid unicodes - 128 + (2048 - 128) + (65536 - 2048) + (2097152 - 65536) = 2097152
  * One to one mapping with 128 ASCII chars in the first byte [backward compatible]

  * Code Points
    - 1-byte - U+0000  to U+007F   - 0xxx xxxx
    - 2-byte - U+0080  to U+07FF   - 110x xxxx 10xx xxxx
    - 3-byte - U+0800  to U+FFFF   - 1110 xxxx 10xx xxxx 10xx xxxx
    - 4-byte - U+10000 to U+10FFFF - 1111 0xxx 10xx xxxx 10xx xxxx 10xx xxxx
    - It's unclear based on what the first few bits are chosen for every byte representation.

  * 1-byte
    - 7-bits - 128 characters are available, ie, ASCII 1-1 mapping

  * 2-byte
    - 11-bit - 2048 characters are possible but only 1920 are available [LSB 7-bits till 0x7F are not available]
      - Allowed chars are given by -> 0x7FF - (0x80 - 1) = 1920
    - Contains almost all remaining Latin script alphabets and IPA extensions
    - All Greek, Cyrillic, Coptic, Armenian, Hebrew, Arabic, Syrian, Thaana and N'Ko alphabets
    - Combining Diacritical Marks

  * 3-byte
    - 16-bits - 65536 characters are possible but only 61440 are available [LSB 11-bits till 0x07FF are not available]
      - Ideally, 63488 should've been available -> 0xFFFF - (0x800 - 1) = 63488
      - 2048 extra encodings are missing - this is between U+D800 and U+DFFF (inclusive)
        - 0xD800 - 1101 1000 0000 0000 -> 1110 xxxx 10xx xxxx 10xx xxxx -> 1110 1101 1010 0000 1000 0000 -> 0xEDA080
        - 0xDFFF - 1101 1111 1111 1111 -> 1110 xxxx 10xx xxxx 10xx xxxx -> 1110 1101 1011 1111 1011 1111 -> 0xEDBFBF
      - [Unicode FAQ](https://www.unicode.org/glossary/#surrogate_code_point)
      - [SO Answer](https://stackoverflow.com/a/40187609)
    - Basic multilingual plane which contains almost all other commonly used characters (eg, Chinese, Japanese, Korean alphabets)

  * 4-byte
    - 21-bits - 2097152 characters are possible but only 1048576 are available 
      - Availability is simply a restriction on the max value -> 0x10FFFF - (0x10000 - 0x1) = 1048576
    - Contains remaining unicodes including historic scripts, mathematical symbols and emojis.

#### Unicode Character -> Code Point Hex/UTF-8 Hex Conversion
  * Ex - Unicode character y, ASCII 79, Code Point U+0079
    - Hex for 0x79 - 111 1001
    - Since this is 7 bits, it has to be 1-byte UTF-8
    - 1-byte UTF-8 hex
      - Relevant 7 bits are filled up in the 'x' starting from LSB, remaining 'x' are padded with 0, hence we get - 0111 1001 -> 0x79

  * Ex - Unicode character À, Code Point U+00C0
    - Hex for 0xC0 - 1100 0000
    - Since this is 8 bits, it has to be 2-byte UTF-8
    - 2-byte UTF-8 hex
      - Relevant 8 bits are filled up in the 'x' starting from LSB, remaining 'x' are padded with 0, hence we get - 1100 0011 1000 0000 -> 0xC380

  * 1-byte to 2-byte/3-byte Conflicts -
    - If required, one can try and store a 1-byte char as a 2-byte char as well - a proposal is to fill the 7 bits in available LSB's first, and then using 0's for the remaining available bits.

    - In 2-byte encoding, 0x79 will be represented as [110]x xxx1 [10]11 1001 - 1100 0001 1011 1001 - 0xC1B9
      - However, 0xC1B9 is not a valid utf-8 [see below]
      - Hence, 2-byte unicodes always start with Code Point Hex 0x80

    - In 3-byte encoding, 0x79 will be represented as [1110] xxxx [10]xx xxx1 [10]11 1001 - 1110 0000 1000 0001 1011 1001 - 0xD081B9
      - However, 0xD081B9 is not a valid utf-8 [see below]
      - 3-byte unicodes always start with Code Point Hex 0x800 (end of 2-byte code point hex)

  * Examples -
    ```
    - 1-byte format                  0xxx xxxx
      Character y   - 0x79        -> 0111 1001
      Relevant bits               ->  111 1001                                  -> U+0079
      2-byte format               -> 110x xxxx 10xx xxxx
      2-byte replacement          ->         1   11 1001
      2-byte value (pad-0)        -> 1100 0001 1011 1001                        -> 0xC1B9 - invalid
      2-byte value (pad-1)        -> 1101 1111 1011 1001                        -> 0xDFB9 - 1 1111 11 1001 -> 0111 1111 1001 -> U+07F9 - valid (߹)


    - 2-byte format                  110x xxxx 10xx xxxx
      Character À   - 0xC380      -> 1100 0011 1000 0000
      Relevant bits               ->    0 0011   00 0000                        -> U+00C0
      3-byte format               -> 1110 xxxx 10xx xxxx 10xx xxxx
      3-byte replacement          ->              0 0011   00 0000
      3-byte value (pad-0)        -> 1110 0000 1000 0011 1000 0000              -> 0xE08380 - invalid
      3-byte value (pad-1)        -> 1110 1111 1010 0011 1000 0000              -> 0xEFA380 -> 1111 10 0011 00 0000 -> 1111 1000 1100 0000 -> U+F8C0 - Unassigned, Private Use


    - 3-byte format                  1110 xxxx 10xx xxxx 10xx xxxx
      Character ᣀ,  - 0xE1A380    -> 1110 0001 1010 0011 1000 0000
      Relevant bits               ->      0001   10 0011   00 0000              -> U+18C0 (CANADIAN SYLLABICS SHOY - ᣀ,)
      4-byte format               -> 1111 0xxx 10xx xxxx 10xx xxxx 10xx xxxx
      4-byte replacement          ->                0001   10 0011   00 0000
      4-byte value (pad-0)        -> 1111 0000 1000 0001 1010 0011 1000 0000    -> 0xF081A380 -> invalid
      4-byte value (pad-1)        -> 1111 0111 1011 0001 1010 0011 1000 0000    -> 0xF7B1A380 -> 111 11 0001 10 0011 00 0000 -> 0001 1111 0001 1000 1100 0000 -> Exceeds limit hence invalid

    - In python, it's easy to get the unicode if UTF-8 hex is available -
      - eg, for UTF-8 hex 0xE1A380, str(b'\xe1\xa3\x80', 'utf-8') will return the relevant unicode.

    ```


### UTF-16, UTF-32 and GB18030
  * UTF-16 is variable length encoding with one or two 2-byte encodings.
    - It isn't ASCII compatible and is not popular.

  * UTF-32 is a fixed length encoding with all representations in 32-bits.
    - Decoding is a constant time operation, however, depending on how commonly the application encounters unicodes beyong 2-byte UTF-8, it's not space efficient.

  * GB18030
    - It's a Chinese government standard - contains all characters necessary for software in China.
    - It's part of UCS (Universal Character Set) and can be mapped to UTF-8 as 1-byte, 2-byte (extended GBK) or 4-byte sequences.

### SCSU - Standard Compression Scheme for Unicode, and BOCU - Binary Ordered Compression for Unicode
  * These are unicode compression schemes to get rid of all the extra bits that are used for encoding unicode chars to UTF-8.
    - Implemented by popular libraries like zip, bzip, gzip
