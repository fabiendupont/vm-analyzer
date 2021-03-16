FROM registry.access.redhat.com/ubi8/ubi

RUN mkdir /data && \
    dnf -y update && \
    rm -rf /var/cache/yum && \
    dnf -y install \
        libguestfs \
        nbdkit \
        nbdkit-plugin-vddk \
        gdb \
        python3 \
        python3-libguestfs &&\
    pip3 install flask \
        flask-restful \
        pyvmomi

COPY vm-analyzer.py /usr/local/bin/vm-analyzer
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY manifest.json /data/manifest.json

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
USER ${USER_UID}
