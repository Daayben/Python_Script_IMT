"""Tests pytest pour la couche données (partie 2)."""

import pytest
from sqlalchemy import create_engine

import annuaire
from annuaire import Base, Domaine, chercher, enregistrer, lister

D1 = Domaine(hote="example.com", ip="93.184.216.34", contact="IANA", email=None)
D2 = Domaine(hote="python.org",  ip="23.253.135.79",  contact=None,   email=None)


@pytest.fixture
def db(tmp_path, monkeypatch):
    """Base SQLite temporaire isolée pour chaque test."""
    moteur = create_engine(f"sqlite:///{tmp_path}/test.db")
    Base.metadata.create_all(moteur)
    monkeypatch.setattr(annuaire, "engine", moteur)
    yield moteur


def test_enregistrer(db):
    enregistrer(D1)
    assert chercher("example.com") == D1


def test_enregistrer_doublon(db):
    enregistrer(D1)
    with pytest.raises(ValueError):
        enregistrer(D1)


def test_lister_vide(db):
    assert lister() == []


def test_lister(db):
    enregistrer(D1)
    enregistrer(D2)
    hotes = [d.hote for d in lister()]
    assert "example.com" in hotes
    assert "python.org" in hotes


def test_chercher_absent(db):
    assert chercher("inconnu.xyz") is None


def test_chercher_present(db):
    enregistrer(D1)
    d = chercher("example.com")
    assert d is not None
    assert d.ip == "93.184.216.34"
    assert d.contact == "IANA"
