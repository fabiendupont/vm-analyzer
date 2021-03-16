FROM centos:8

RUN mkdir /data && \
    yum -y update && \
    rm -rf /var/cache/yum && \
    yum -y install epel-release && \
    yum -y install \
        libguestfs \
        nbdkit \
        nbdkit-plugin-vddk \
        python3 \
        gdb \
        python3-libguestfs &&\
    yum clean all && \
    pip3 install flask \
        flask-restful \
        pyvmomi

COPY vm-analyzer.py /usr/local/bin/vm-analyzer
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY manifest.json /data/manifest.json

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
USER ${USER_UID}

