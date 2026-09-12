## Summary

- This is pretty much the same project as my motion activated Jarvis using an Arduino board 
- The only difference is that this one is purely voice activated, no board needed. All you  need to do is to say `Jarvis` to active the commands

## Commands

- What time is it?
  - tells local time

- What is my name?
  - tells you the name to call you 
  - by default it is Mr. Bibb

- Change my name.
  - allows you to set a custom name to be called

- Create a text file.
  - allows you to create a txt file, and set its contents, inside the directory the program lives

- Open a text file.
  - allows you to open and read the contents of a txt file in the directory the program lives

- Start a time
  - allows you to set a time and a customer time and alerts you when timer is finished

- Optimize
  - this commands allows you to use an actually AI model, rather than the built in commands seen above. All you need to do is say the commands `optimize`, then follow that with another command of your choice after the voice response from Jarvis
  - optiized commands are cached as to not spam API requests to the AI model. Any command that has a successful cache hit will replay the same response as before.  




