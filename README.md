
# PS1Decoder
This python script deobfuscate PowerShell scripts.

## Characteristic
- Deobfuscate ASCII base64 encode.
- Deobfuscate Unicode base64 encode.
- Rename obfuscated variables according to their entropy.
- Rename variables according to their type (string, string concat, int, float, null, true, false, new object).
- Rename functions.

## Usage
    python PS1Decoder.py input

## Example
Obfuscate PowerShell script

    ${global:ZPpMXBycE4mCNYa9o6mP}  =  9831
    ${private:wal8i4pdFxdMvO6gb4PI}  =  "hello world"
    ${private:eL78KxptJvgUzUpTbJJU}  =  4.1
    $secret = $([Text.Encoding]::ASCII.GetString([Convert]::FromBase64String('LjpVTkQzUjou')))

Deobfuscate PowerShell script

    ${global:var_int_9831_1}  =  9831
    ${private:var_str_hello_world_1}  =  "hello world"
    ${private:var_float_4__1_1}  =  4.1
    $secret  =  ".:UND3R:."

## License
[GNU General Public License v3.0](https://raw.githubusercontent.com/victorgutierrez92/PS1Decoder/master/LICENSE)