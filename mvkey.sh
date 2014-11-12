#!/bin/sh

echo 'This command is not compatible with any scp flags. Set up the ssh connection in your ssh config first.'
echo ''
decider=false
if [ "${1##*.}" != "pub" ]; then
 read -p "$1 doesn't have a .pub ending and may not be a public key. Do you want to continue? [Y/n] " yn
 case $yn in
   [Nn]* ) ;;
       * ) decider=true;;
 esac
else
 decider=true
fi
if [ $decider == true ] && [ $(scp $1 $2) ]; then
  rm $1
  read -p "Do you want to directly append the key to the remote authorized_keys? [y/N]" yn
  case $yn in
      [Yy]* ) if [ ssh $(echo $2 | cut -d ':' -f1) -t $(echo 'cd ')$(echo $(echo $2 | cut -d ':' -f2))$(echo '; cat ')$(echo $1)$(echo '>> authorized_keys; rm ')$(echo $1) ]; then
                echo "appended $1 to remote authorized_keys"
              fi;;
          * ) echo $(echo 'connecting to ')$(echo $2)
              ssh $(echo $2 | cut -d ':' -f1) -t $(echo 'cd ')$(echo $(echo $2 | cut -d ':' -f2))$(echo '; $SHELL -l');;
  esac
fi
