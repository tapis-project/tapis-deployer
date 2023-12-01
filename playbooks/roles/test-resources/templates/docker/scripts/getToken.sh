#!/bin/bash
#set -xv
TENANT=dev
ENDPOINT=v3/oauth2/tokens
URL=https://${TENANT}.{{ global_tapis_domain }}/${ENDPOINT}

function usage() {
  echo "$0 [-t tenant] [-p password] [-u user] [--base-url]"

  echo "OPTIONS:"
  echo "    -t --tenant"
  echo "        The tenant to use for the request"
  echo 
  echo "     -u --username"
  echo "        The username to use for the request"
  echo 
  echo "     -p --password"
  echo "        The password to use for the request"
  echo 
  echo "     -b --base-url"
  echo "        The base url to use for the request.  Defaults to 'https://${TENANT}.{{ global_tapis_domain }}/${ENDPOINT}'"
  echo 
  echo "     -v --verbose"
  echo "        echo command before executing it"
  exit 1
}


while [[ $# -gt 0 ]]; do
  case $1 in
    -t|--tenant)
      TENANT="$2"
      shift # past argument
      shift # past value
      ;;
    -b|--base-url)
      URL="$2"
      shift # past argument
      shift # past value
      ;;
    -p|--password)
      PASSWORD="$2"
      shift # past argument
      shift # past value
      ;;
    -u|--username)
      USERNAME="$2"
      shift # past argument
      shift # past value
      ;;
    -v|--verbose)
      IS_VERBOSE=true
      shift # past argument
      ;;
    -*|--*)
      echo "Unknown option $1"
      usage
      ;;
#    *)
#      POSITIONAL_ARGS+=("$1") # save positional arg
#      shift # past argument
#      ;;
  esac
done

if [[ -z ${USERNAME} ]] ; then
  usage
else
  # echo to stderr
  echo >&2 Using username: \"${USERNAME}\"
fi

if [[ -z ${PASSWORD} ]] ; then 
  # prompt on stderr
  echo -n >&2 Enter Password: 
  read -rs PASSWORD
fi

if [[ -z ${USER} || -z ${PASSWORD} ]] ; then
  echo
  echo username and password are required
  usage
fi

if [[ ${IS_VERBOSE} ]] ; then 
  echo >&2 "http --check-status ${URL} Content-type:application/json username=${USERNAME} password=${PASSWORD} grant_type=password"
fi

RESULT=$(http --check-status ${URL} Content-type:application/json username=${USERNAME} password=${PASSWORD} grant_type=password)
EXIT_CODE=$?
if [[ ${EXIT_CODE} -ne 0 || -z $RESULT ]] ; then 
  echo >&2 No token returned
  echo >&2 ${RESULT}
  echo >&2 exit code ${EXIT_CODE}
  exit ${EXIT_CODE}
else
  TOKEN=`echo ${RESULT} | jq -r ".result[] | (.access_token)"`
  echo ${TOKEN}
fi


