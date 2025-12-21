{
  pkgs ? import <nixpkgs> { },
}:

let
  python = pkgs.python3;
in
python.pkgs.buildPythonPackage {
  pname = "pypartial";
  version = "0.1.0";
  src = ./.;
  format = "pyproject";

  nativeBuildInputs = with python.pkgs; [
    setuptools
    wheel
    pip
  ];

  propagatedBuildInputs = with python.pkgs; [
    pydantic
  ];

  checkInputs = with python.pkgs; [
    pytest
  ];
}
