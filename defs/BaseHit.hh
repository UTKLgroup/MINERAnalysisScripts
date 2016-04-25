#ifndef _BASEHIT_H
#define _BASEHIT_H

#include "TObject.h"
#include "TLorentzVector.h"
#include "TVector3.h"

class BaseHit : public TObject {
private:
    TVector3 _pos;
    TVector3 _3mom;
    int _pid;
    float _edep;
    float _ekin;
    float _weight;
    int _detID;
    float _time;
    int _inc;
    int _pre;
    int _post;

public:
    BaseHit();
    virtual ~BaseHit();

    // "get" methods -----------

    TVector3 pos() const;
    TVector3 p3() const;
    int pid() const;
    float Weight() const;
    float Edep() const;
    float Ekin() const;
    int detID() const;
    float time() const;
    int inc() const;
    int preproc() const;
    int postproc() const;

    // "set" methods ---------
    void SetPos(float vx, float vy, float vz);
    void Setp3(float px, float py, float pz);
    void SetEdep(float e);
    void SetEkin(float e);
    void SetPid(int id);
    void SetDetID(int d);
    void SetTime(float t);
    void SetInc(int i);
    void SetWeight(float w);
    void SetPreProcess(int p);
    void SetPostProcess(int p);

    ClassDef(BaseHit, 1);


};

#endif  /* _BASEHIT_H */
