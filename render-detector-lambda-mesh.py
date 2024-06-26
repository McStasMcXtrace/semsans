import numpy as np
from plotoptix import TkOptiX
from plotoptix.enums import DenoiserKind
from plotoptix.utils import map_to_colors
from definitions import *

DENOISE = False
def main():
    R = 3000
    path = f'scattering_data/{R}/0/det.dat'
    params = extract_parameters(path)
    y, _,_,_ = np.genfromtxt(path, delimiter=' ', usecols=(0,1,2,3), unpack=True)

    N_lambda = 500
    N_y = len(y)
    I = np.zeros((N_lambda, N_y))
    lambdas = np.zeros((N_lambda))
    # lambdas
    print(f"Visualizing with {N_y} y points and {N_lambda} lambda points")
    for i in range(N_lambda):
        path = f'scattering_data/{R}/{i}/det.dat'
        params = extract_parameters(path)
        y, _,_,I[i,:] = np.genfromtxt(path, delimiter=' ', usecols=(0,1,2,3), unpack=True)
        lambdas[i] = float(params['L0'])
    print(I.shape)
    # Y = I * 3e13
    Y = I / 20000 * 75
    x = lambdas
    # y = lambdas
    rx = (np.min(x), np.max(x))
    rz = (np.min(y), np.max(y)) 
    print(rx, rz)
    print(rx, rz)
    # rz = (-10, 10)

    rt = TkOptiX() # create and configure, show the window later

    rt.set_param(max_accumulation_frames=1000)  # accumulate up to 50 frames
    rt.set_background(0) # black background
    rt.set_ambient(1.0) # some ambient light

    # try commenting out optional arguments
    rt.set_data_2d("surface", Y,
                   range_x=rx, range_z=rz,
                   c=map_to_colors(Y, "cividis"),
                #    floor_c=[0.0,0.0,0.0],
                #    floor_y=-1.75,
                #    make_normals=True
                  )
    rt.setup_camera("cam1", cam_type="DoF",
                # eye=[-50, -7, -15], target=[0, 0, -1], up=[0, 1, 0],
                aperture_radius=0.4, aperture_fract=0.2,
                focal_scale=0.92, fov=35, glock=True)

    eye = rt.get_camera_eye()
    eye[1] = 0.5 * eye[2]
    rt.update_camera("cam1", eye=eye)

    d = np.linalg.norm(rt.get_camera_target() - eye)
    rt.setup_light("light1", color=8, radius=0.3 * d)

    if DENOISE:
    # AI denoiser includes exposure and gamma corection, configured with the
        # same variables as the Gamma postprocessing algorithm.
        rt.set_float("tonemap_exposure", 0.5)
        rt.set_float("tonemap_gamma", 2.2)

        # Denoiser blend allows for different mixing with the raw image. Its value
        # can be modified also during the ray tracing.
        rt.set_float("denoiser_blend", 0.0)

        # Denoising is applied by default after the 4th accumulation frames is completed.
        # You can change the starting frame with the following variable:
        rt.set_uint("denoiser_start", 12)

        # Denoiser can use various inputs. By default it is raw RGB and surface
        # albedo, but not always it results with the optimal output quality.
        # Try one of the below settings and find best configuration for your scene. 
        #rt.set_int("denoiser_kind", DenoiserKind.Rgb.value)
        #rt.set_int("denoiser_kind", DenoiserKind.RgbAlbedo.value)
        rt.set_int("denoiser_kind", DenoiserKind.RgbAlbedoNormal.value)

        #rt.add_postproc("Denoiser")
        #rt.add_postproc("DenoiserHDR")
        # rt.add_postproc("DenoiserUp2x")
        rt.add_postproc("OIDenoiser")
        #rt.add_postproc("OIDenoiserHDR")

    # Postprocessing stages are applied after AI denoiser (even if configured
    # in a different order).
    rt.set_float("levels_low_range", 0.1, 0.05, -0.05)
    rt.set_float("levels_high_range", 0.95, 0.85, 0.8)
    rt.add_postproc("Levels")
    # rt.set_coordinates()

    # 3. Tonal correction with a custom curve.
    #rt.set_float("tonemap_exposure", 0.8)
    #rt.add_postproc("GrayCurve")
    rt.start()

    print("done")

if __name__ == '__main__':
    main()