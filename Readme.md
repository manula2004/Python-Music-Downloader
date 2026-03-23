# InfoLanka Music Downloader



A Python script to download Sri Lankan songs in \*\*Real Audio (.ra/.ram)\*\* format from \[InfoLanka Miyuru Gee](http://www.infolanka.com/miyuru\_gee/). It automatically processes `.ram` files, renames them using metadata, and cleans up temporary files.



\## Features



\- \*\*Artist Listings\*\*: Fetches all artists available on the InfoLanka site.

\- \*\*Selection System\*\*: Choose artists by a simple numbered list.

\- \*\*Auto-Processing\*\*: 

&#x20; - Downloads `.ra` and `.ram` files automatically.

&#x20; - Parses `.ram` files to extract the underlying `.ra` URLs.

\- \*\*Smart Renaming\*\*: Uses metadata to rename files (e.g., `Artist - Title.ra`).

\- \*\*Multithreading\*\*: High-performance concurrent downloads.



\## Requirements



\- \*\*Python 3.10+\*\*

\- \*\*FFmpeg\*\*: `ffprobe` must be available in your system `PATH`.

\- \*\*Internet Connection\*\*



\## Installation



1\. Clone or download this repository.

2\. Ensure `ffprobe` is installed and accessible via command line.

3\. No external Python libraries are required (uses standard `urllib` and `subprocess`).



\## Usage



1\. Open a terminal in the project directory.

2\. Run the script:

&#x20;  ```bash

&#x20;  python music.py

&#x20;  ```



\### Operational Flow:

\- Fetch artist list -> Select by number -> Download -> Rename -> Cleanup.



\## Example Output



```text

Starting audio file processor...

Found 300 artists:

1\. Aathma Liyanage

2\. Abewardhana Balasuriya

3\. Amaradeva W. D.

...

Choose artist number: 3

Selected: Amaradeva W. D.

Found 25 files

Downloaded: song1.ra

Renaming files...

Renamed: Amaradeva W. D. - Song1.ra

Done!

```



> \[!NOTE]

> If metadata is missing, the script will preserve the original filename.



> \[!TIP]

> You can adjust `MAX\_WORKERS` within `fullw.py` to optimize download speeds for your connection.



\## License

This script is for personal use only. Please respect the copyrights of artists and the hosting platform.

