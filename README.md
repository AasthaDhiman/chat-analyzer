# chat-analyzer
This tool helps you analyze WhatsApp chat exports in a fun and meaningful way using Python and Streamlit (a tool to make web apps).
This process involves following steps-
1-Preprocessing the chat-
   Reads the WhatsApp chat file.
   Extracts:Date and Time,User Name,Message Content
   Adds useful information like:
   Day, Month, Year
   Time (Hour, Minute)
   Day of the week (e.g., Monday)

2-Chat Statistics-
  It shows-Total messages sent,Total words used,Media files shared,Links shared

3-Timeline Analysis-
  Which day of the week is most active?
  Which month is the busiest?
  For group chats, it shows who sent the most messages.
  Also shows percentage contribution.

4-Wordcloud-
  Visual representation of the most used words.
  Bigger words = used more often.

What It Needs From You:
1.A WhatsApp chat export (.txt file)
2.You upload it in the sidebar, and it does the rest!
