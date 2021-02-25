{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.hello
    (pkgs.python3.withPackages (ps: with ps; [numpy python-language-server pyls-mypy]))
    # keep this line if you use bash
    pkgs.nixfmt
    pkgs.bashInteractive
  ];
}
