#include "BaseTrack.hh"
#include <iostream>

BaseTrack::BaseTrack() {

}

BaseTrack::~BaseTrack() {

}



// "get" methods -------------------------------------

TLorentzVector BaseTrack::p4() const {
   return _4mom;
}

float BaseTrack::E() const {
   return _4mom.E();
}

float BaseTrack::p() const {
   return _4mom.P();
}

TVector3 BaseTrack::pos() const {
   return _pos;
}

int BaseTrack::pid() const {
   return _pid;
}

float BaseTrack::time() const {
   return _time;
}

int BaseTrack::inc() const {
   return _inc;
}

// "set" methods ---------------------------------------------

void BaseTrack::Setp4(TLorentzVector mom) {
   _4mom = mom;
}

void BaseTrack::SetInc(int i) {
   _inc = i;
}

void BaseTrack::Setp4(float px, float py, float pz, float e) {
   TLorentzVector mom(px, py, pz, e);
   _4mom = mom;
}

void BaseTrack::SetPos(float vx, float vy, float vz) {
   TVector3 v3(vx, vy, vz);
   _pos = v3;
}

void BaseTrack::SetPid(int id){
   _pid = id;
}

void BaseTrack::SetTime(float t) {
   _time = t;
}
