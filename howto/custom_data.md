## Prepare Custom Data

#### 3.1 Get Pretrained Model Files from PIXIE and SMPLX (follow multiview_optimization md in repo)
	1. create accounts on their websites (I recommend with same email and password)
		- https://pixie.is.tue.mpg.de/
		- https://smpl-x.is.tue.mpg.de/

	2. follow the Manual on PIXIE https://github.com/yfeng95/PIXIE/blob/master/Doc/docs/getting_started.md

	3. copy the following files into your repo in multiview_optimization
		-  SMPL-X__FLAME_vertex_ids.npy 
		-  smplx_extra_joints.yaml
		-  SMPLX_NEUTRAL_2020.npz

	4. change the path to them in `utils/config.py`

```python
12 	    cfg.pixie_dir = /path/to/dir/
```

#### 3.2 PIXIE: initialization_pixie



#### 3.3 Colmap (optional)