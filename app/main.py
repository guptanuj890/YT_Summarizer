from classifier import classify_video

transcript_text = """
    Chapter 1: Trump's controversial cap
0:000 secondsAmid the war in West Asia, a political storm has erupted in the United States and it centers around President Trump
0:077 secondsand a baseball cap. California Governor Gavin Newsome sharply criticized Trump over his conduct at a solemn military
0:1515 secondsceremony. The criticism came after Trump attended a dignified transfer ceremony at Dover Air Force Base in Delaware,
0:2323 secondswhich honored six American soldiers killed in the conflict linked to Iran.
0:2828 secondsTrump attended the ceremony last Saturday. He was joined by First Lady Melania Trump and the families of the
0:3434 secondsfallen troops. A dignified transfer is one of the most solemn duties for a US president. It marks the return of
0:4242 secondsservice members killed in action to American soil, but the president's appearance sparked outrage. Donald Trump
0:4949 secondswore a white baseball cap. The cap had USA embroidered in gold thread. He kept the cap on as the flag draped coffins
0:5858 secondswere carried past. Some observers also noted that Trump did not bow his head while others did.
Chapter 2: Backlash and defense
1:171 minute, 17 secondsThe California governor's press office reacted on outrage on X. Gavin Newsome's office shared a video of the ceremony,
1:241 minute, 24 secondswriting, "Take your hat off, you disgusting little man." Even Trump's niece, Mary Trump, criticized the
1:311 minute, 31 secondspresident. She called him an unspeakable disgrace. And the moment triggered a wave of reactions online. Former
1:381 minute, 38 secondsRepublican National Committee chairman also condemned Trump. He wrote that the ceremonies called a dignified transfer for a reason. Many commentators agreed.
1:491 minute, 49 secondsThey said the president should have removed his hat, but some supporters defended Trump. They said his presence mattered more than the hat. The ceremony
Chapter 3: Deepening conflict and toll
1:581 minute, 58 secondshonored six US Army Reserve soldiers killed in Kuwait. The strike came one day after United States and Israel
2:052 minutes, 5 secondslaunched military operations against Iran. Meanwhile, the toll on American forces has risen again. The Pentagon
2:122 minutes, 12 secondsconfirmed yesterday that a seventh US service member had died. The soldier had been seriously wounded during Iranian
2:192 minutes, 19 secondsattacks earlier in the conflict. The identity of the soldier has not yet been released.
2:262 minutes, 26 secondsSo, as the war deepens and casualties rise, the debate over Trump's conduct at a solemn ceremony has only intensified
2:342 minutes, 34 secondsthe political battle in the United States. Want the facts? The latest developments. News that gets straight to the point.
2:422 minutes, 42 secondsWell, we've got all three just for you.
2:442 minutes, 44 secondsThis is First Post Live, a brand new show. Your window into what really matters. Don't miss it.


"""
result = classify_video(transcript_text)

print("Video type", result.choice)
print("probabilities", result.probabilities)