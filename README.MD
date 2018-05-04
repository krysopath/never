# never

used as yet another credential store. create entries and have secrets generated for them. access those over ssh.

## install
- install `anakin` and `dbio`
- `python3 setup.py install`

## operation
1. let people access the ssh service, which executes `never $username` for them to give them access 
2. use it locally, by running the `broker $fancynamespace`
3. access it via json requests (not yet)
4. run it inside docker. no problems!


