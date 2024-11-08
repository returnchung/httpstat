NAME="httpstat";
TAG=$(git rev-parse --short HEAD);

# Get the current credential config and the latest username
REPO=${DOCKER_REPOSITORY:-return1225};
# Setup default port and respect the environment.
_PORT=${PORT:-32767};

LATEST_TAG=latest;
if [ -z "$TAG" ]
then
    TAG=$(date +%Y%m%d%H%M);
fi

for arg in $@;
do
    case "$arg" in
        build) build=1
            docker image pull $REPO/$NAME:$TAG;
            if [ $? -eq 1 ]
            then
                echo "### Build image >>>";
                docker image build . -t $REPO/$NAME:$TAG --platform=linux/amd64;
                docker image tag $REPO/$NAME:$TAG $REPO/$NAME:$LATEST_TAG;
            fi
            ;;
        push) push=1
            echo "### Push image $REPO/$NAME:$TAG >>>";
            docker image push $REPO/$NAME:$TAG;
            docker image push $REPO/$NAME:$LATEST_TAG;
            ;;
        run) run=1
            CTNER=$(docker container ls -a | grep $NAME | awk '{print $1}');
            if [ ! -z "$CTNER" ]
            then
                echo "### Remove container before running ...";
                docker container rm -f $CTNER;
            fi
            docker container run -d \
                --name $NAME \
                -p $_PORT:$_PORT \
                --restart=unless-stopped \
                $REPO/$NAME:$TAG;
            ;;
        *) echo "unknown args: $arg";;
    esac
done
