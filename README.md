Predict word
========

Python program to predict next word of sentence (base on corpus input) , and when speak it.


Build
-----

    $ XSOCK=/tmp/.X11-unix
    $ XAUTH=/tmp/.docker.xauth
    $ xauth nlist :0 | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -

    $ docker build . -t predict_image
    $ docker run --rm -d --name predict -v $XSOCK:$XSOCK -v $XAUTH:$XAUTH -e XAUTHORITY=$XAUTH -v $(pwd):/shared --device /dev/snd predict_image
    $ docker exec -ti predict bash
    $ ebook-convert corpus/epub/doc.epub corpus/txt/corpus.txt
    $ python3 predict.py corpus/txt/corpus.txt
    $ predict corpus/txt/corpus.txt