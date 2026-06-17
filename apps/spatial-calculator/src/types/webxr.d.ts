interface Navigator {
  xr?: XRSystem;
}

interface XRSystem {
  isSessionSupported?: (mode: XRSessionMode) => Promise<boolean>;
}

type XRSessionMode = "inline" | "immersive-ar" | "immersive-vr";
