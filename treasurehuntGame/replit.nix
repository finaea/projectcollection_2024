{ pkgs }: {
    deps = [
      (pkgs.haskellPackages.ghcWithPackages (pkgs: [
      pkgs.random ]))
      pkgs.haskell-language-server
    ];
}