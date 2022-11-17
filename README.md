# ChaCha20
Aaron Fihn, Prateep Malyala, Shang Xiao, Nathaniel Webb

The inputs to ChaCha20 are:
   o  A 256-bit key, treated as a concatenation of eight 32-bit little-
      endian integers.
   o  A 96-bit nonce, treated as a concatenation of three 32-bit little-
      endian integers.
   o  A 32-bit block count parameter, treated as a 32-bit little-endian
      integer.

   The output is 64 random-looking bytes.





Acknowledgements:
1. https://sciresol.s3.us-east-2.amazonaws.com/IJST/Articles/2016/Issue-3/Article24.pdf