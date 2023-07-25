# Kreuzwort

This tool aims to generate a complete arrowword puzzle from a list of words. I first got the idea for this when I was teaching English to classes of young children and needed a regular, heads-down activity to practice vocabulary. The coursebook I was using at the time had a few arrowords that the kids loved, but they were used up within weeks. I did, however, have a wordlist with definitions for every single unit of the book, which was also available in the form of a spreadsheet. I figured I could easily write a short script that would take this list and turn it into a puzzle. Turns out it's a little more complicated than that.

This was one of my first large-ish scale projects, and it has been attempted and rewritten a few times. I have come across many issues that seemed insurmountable at the time, only to find simple solutions for them after further study and thinking things over. The reason I decided to start again from scratch is that I have since moved on to Test Driven Development, and wanted to apply what I've learned here. And that means starting from scratch, with failing tests.

At this stage, I am exploring methods of sorting the given words according to their "quality", which may mean the number of letters they have in common with other words, or the frequency of the list's most common letter in one particular word, or maybe even other aspects I haven't thought of yet.
The reason for this initial data-gathering is that eventually, I want the word placement algorithm to be able to choose from a list of options for the next word, potentially choosing one, trying placement, and being able to backtrack along a "history" of sorts to an earlier point from where it can restart in case of issues. This might even lead to several possible solutions being created, which can then be filtered according to things like the size of the table.

In the long term, I'd like to also incorporate the ability to output a formatted table in, for example, HTML so that I can print/publish these crosswords. I might even write some sort of interface so that others can easily input wordlists and receive finished arroword puzzles.
