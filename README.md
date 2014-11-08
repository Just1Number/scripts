## scripts
A collection of scripts

### mvkey
`mvkey` is a script to make the deployment of ssh keys a bit simpler.

It does the following things:

1. Give a warning if the key you want to copy onto a server doesnt have the .pub file extention
2. Copy the key
3. Ask if you want to remove it localy
4. Directly appends the key to the remote `authorized_keys` file or connects directly via ssh into the remote directory you just copied the key to

The syntax is identical to `scp` without any flags:

`mvkey publickey [user@]host:path/to/where/publickeys/go`

You can copy mvkey to /bin or or as a function to your .<shell>rc (.zshrc /.bashrc).
