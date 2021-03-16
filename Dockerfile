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
    yum -y debuginfo-install python36-3.6.8-2.module_el8.3.0+562+e162826a.x86_64 && \
    yum clean all && \
    pip3 install flask \
        flask-restful \
        pyvmomi

COPY vm-analyzer.py /usr/local/bin/vm-analyzer
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY manifest.json /data/manifest.json

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
USER ${USER_UID}

