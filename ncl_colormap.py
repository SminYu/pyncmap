import os
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm

class ColorMapMaker:
    """
    Colormap 이름과 데이터 경로를 기반으로 Matplotlib의 컬러맵,
    정규화(norm), 경계(boundaries)를 관리하는 클래스입니다.

    사용 예시:
    >>> cbar = ColorMapMaker('my_cmap_r')
    >>> cmap = cbar.cmap
    >>> norm = cbar.norm
    >>> boundaries = cbar.boundaries
    >>> # 또는 한 번에 가져오기
    >>> cmap, norm, boundaries = cbar.get_all()
    >>> plt.pcolormesh(data, cmap=cmap, norm=norm)
    """
    def __init__(self, name: str, data_dir: str = None):
        """
        Args:
            name (str): 불러올 컬러맵의 이름. 이름 끝에 '_r'을 붙이면 색상 순서가 반전됩니다.
            data_dir (str, optional): cmap 데이터 파일(.rgb, .bound)이 있는
                                      디렉토리 경로. 지정하지 않으면 이 파일과
                                      동일한 경로의 'cmap_data' 폴더를 사용합니다.
        """
        self.name = name
        self._reverse = name.endswith('_r')
        self._base_name = name[:-2] if self._reverse else name

        if data_dir is None:
            # 스크립트가 실행되는 위치를 기준으로 'cmap_data' 폴더 경로를 설정합니다.
            cwd = os.path.dirname(os.path.abspath(__file__))
            self._data_path = os.path.join(cwd, 'cmap_data')
        else:
            self._data_path = data_dir

        # 결과를 캐싱하기 위한 내부 변수
        self._cmap = None
        self._boundaries = None
        self._norm = None

    @staticmethod
    def _is_float(element: any) -> bool:
        """문자열이 float으로 변환 가능한지 확인하는 정적 헬퍼 메서드"""
        try:
            float(element)
            return True
        except ValueError:
            return False

    @property
    def cmap(self) -> ListedColormap:
        """컬러맵 객체 (ListedColormap)를 반환합니다. 첫 호출 시 파일을 읽어 생성합니다."""
        if self._cmap is None:
            rgb_file = os.path.join(self._data_path, f'{self._base_name}.rgb')
            with open(rgb_file, 'r') as f:
                lines = f.readlines()

            li_rgb = []
            for line in lines:
                # 공백으로 분리된 숫자들을 float 리스트로 변환
                colors = [float(s) for s in line.split() if self._is_float(s)]
                if len(colors) == 3:
                    li_rgb.append(colors)
            
            if self._reverse:
                li_rgb = list(reversed(li_rgb))

            data = np.array(li_rgb)
            # 데이터를 최대값으로 나누어 0-1 사이로 정규화
            data = data / np.max(data)
            self._cmap = ListedColormap(data, name=self.name)
        return self._cmap

    @property
    def boundaries(self) -> list:
        """경계 값 리스트를 반환합니다. 첫 호출 시 파일을 읽어 생성합니다."""
        if self._boundaries is None:
            bound_file = os.path.join(self._data_path, f'{self._base_name}.bound')
            with open(bound_file, 'r') as f:
                # list comprehension을 사용하여 더 간결하게 작성
                self._boundaries = [float(line.strip()) for line in f]
        return self._boundaries

    @property
    def norm(self) -> BoundaryNorm:
        """정규화 객체 (BoundaryNorm)를 반환합니다. 첫 호출 시 생성합니다."""
        if self._norm is None:
            # .cmap과 .boundaries 속성을 사용하여 BoundaryNorm 객체 생성
            self._norm = BoundaryNorm(self.boundaries, self.cmap.N, clip=True)
        return self._norm

    def get_all(self) -> tuple:
        """컬러맵, 정규화 객체, 경계 리스트를 튜플로 한 번에 반환합니다."""
        return self.cmap, self.norm, self.boundaries
