#include "BaseHit.hh"
#include <iostream>

BaseHit::BaseHit() {

}

BaseHit::~BaseHit() {

}



// "get" methods -------------------------------------


TVector3 BaseHit::pos() const {
   return _pos;
}

TVector3 BaseHit::p3() const {
   return _3mom;
}

int BaseHit::pid() const {
   return _pid;
}

float BaseHit::Weight() const {
   return _weight;
}

float BaseHit::Edep() const {
   return _edep;
}

float BaseHit::Ekin() const {
   return _ekin;
}

int BaseHit::detID() const {
   return _detID;
}

float BaseHit::time() const {
   return _time;
}

int BaseHit::inc() const {
   return _inc;
}

int BaseHit::preproc() const {
   return _pre;
}

int BaseHit::postproc() const {
   return _post;
}

// "set" methods ---------------------------------------------

void BaseHit::SetInc(int i) {
   _inc = i;
}

void BaseHit::SetPos(float vx, float vy, float vz) {
   TVector3 v3(vx, vy, vz);
   _pos = v3;
}

void BaseHit::Setp3(float px, float py, float pz) {
   TVector3 mom(px, py, pz);
   _3mom = mom;
}

void BaseHit::SetPid(int id){
   _pid = id;
}

void BaseHit::SetWeight(float w) {
   _weight = w;
}


void BaseHit::SetDetID(int d) {
   _detID = d;
}

void BaseHit::SetTime(float t) {
   _time = t;
}

void BaseHit::SetEdep(float e) {
   _edep = e;
}

void BaseHit::SetEkin(float e) {
   _ekin = e;
}

void BaseHit::SetPreProcess(int p) {
   _pre = p;
}

void BaseHit::SetPostProcess(int p) {
   _post = p;
}
