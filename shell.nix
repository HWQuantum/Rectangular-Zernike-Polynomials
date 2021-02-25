{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.hello
    (pkgs.python3.withPackages (ps: with ps; [numpy]))
    # keep this line if you use bash
    pkgs.nixfmt
    pkgs.bashInteractive
  ];
}
