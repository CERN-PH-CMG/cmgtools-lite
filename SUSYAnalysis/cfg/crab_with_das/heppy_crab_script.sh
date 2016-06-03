#!/bin/sh
echo $HOME
echo $CMSSW_BASE
 
# extract exported necessary stuff
#tar xzf cmgdataset.tar.gz --directory $HOME
tar xzf python.tar.gz --directory $CMSSW_BASE
#tar xzf cafpython.tar.gz --directory $CMSSW_BASE

# uncomment for debuging purposes

#ls -lR .

mv -i src/* $CMSSW_BASE/src/
echo "ARGS:"
echo $@
echo "ENV..................................."
env
echo "VOMS"
voms-proxy-info -all
echo "CMSSW BASE, python path, pwd, home"
echo $CMSSW_BASE
echo $PYTHONPATH
echo $PWD
echo $HOME

# copy auxiliarity data to the right place (json, pu, lep eff, jet corr, ...)
cp lib/slc*/* $CMSSW_BASE/lib/slc*
for i in `find src/ -name data -type d`
do
    echo $i
    mkdir -p  $CMSSW_BASE/$i
    cp -r $i/* $CMSSW_BASE/$i
done

#ls -lR 
PROXYFILE=`grep "BEGIN CERTIFICATE" * | perl -pe 's/:.*//'  | grep -v heppy | tail -n 1`
export X509_USER_PROXY=$PWD/$PROXYFILE
echo Found Proxy in: $X509_USER_PROXY
MD5SUM=`cat python.tar.gz heppy_config.py | md5sum | awk '{print $1}'`

cat <<EOF > fakeprov.txt
Processing History:
 HEPPY '' '"CMSSW_X_y_Z"' [1]  ($MD5SUM)
EOF

cat <<EOF > $CMSSW_BASE/bin/$SCRAM_ARCH/edmProvDump
#!/bin/sh
cat fakeprov.txt
EOF

chmod +x $CMSSW_BASE/bin/$SCRAM_ARCH/edmProvDump

echo "Which edmProvDump"
which edmProvDump
edmProvDump

# Update library path
# Needed so recompiled modules are found
export LD_LIBRARY_PATH=./lib/${SCRAM_ARCH}:$LD_LIBRARY_PATH 
#export LD_LIBRARY_PATH=./lib/slc6_amd64_gcc481:$LD_LIBRARY_PATH 
echo $LD_LIBRARY_PATH

echo $@

#root -l -b <<EOF
#.include
#EOF

python -u heppy_crab_script.py $@
echo "After heppy_crab_script.py"
echo "Output/cmsRun.log:"
cat Output/cmsRun.log

echo "Now removing Output/cmsswPreProcessing.root"
rm -rf ./Output/cmsswPreProcessing.root
ls -lR

