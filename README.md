# cnsr-tagging-tool

A simple media player where one can tag the beginning and the end of the problematic segment in the video.
-

# The media player
The media player is implemented via python's PyQt5 library, it is a simple video player which consists of:

- A video streamer.

- A bar which represents the time.

- One 'Start' button to tag where the problematic segment begins.

- Second 'Finish' button to tag where the problemtac segment ends.

- ScrollDown list which has four tagging specification:
    
   1 - Violance.
   
   2 - Verbal abuse.
   
   3 - Nudity.
   
   4 - Alcohol and drups consumption.
    

# The format creator

The program will save all the tagged segments in timestamps, with dividing '-' 

character between the 'begin' timestamp and the 'finish' time stamp.

After that, the program will export a cnsr file which consists of all the tags with their spacifiction,

printed row by row.
