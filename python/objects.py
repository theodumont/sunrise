# coding: utf8

from utils import rotation, init_sommets
import decorators as dec
import matplotlib.pyplot as plt
print(">> Loading module: 'objects'...")


class Objet3d:

    def __init__(self, dimensions):
        """
        initializes a 3d object
        USING: - Coord6d
               - init_sommets
        """
        pass


class Mobile(Objet3d):

    def __init__(self, dimensions):
        """
        initializes a mobile
        voir si l'on a besoin d'attributs supplémentaires
        """
        Objet3d.__init__(self, dimensions)

    def move(self, spatial, angular):
        """
        moves the mobile
        USING: - change_spatial
               - change_angular
        """
        pass


class Hangar(Objet3d):

    def __init__(self, dimensions):
        """
        initializes the hangar
        USING: - Coord6d
        """
        Objet3d.__init__(self, dimensions)


class Coord6d:

    def __init__(self, x=0, y=0, z=0, alpha=0, beta=0, gamma=0):
        """
        initializes the 6 coordinates
        """

    def change_spatial(self, spatial):
        """
        change the angular coordinates
        cf reconstruction_coins
        """
        pass

    def change_angular(self, angular):
        """
        change the angular coordinates
        USING: - rotation
        cf reconstruction_coins
        """
        pass


class Trajectoire:

    def __init__(self, type, array):
        """
        Class constructor
        """
        self._type = type  # Accessible uniquement en lecture
        self.array = array
        pass

    @property
    def type(self):
        """
        Accéder en lecture à type
        """
        return self._type

    def __str__(self):
        """
        Prettily display a trajectory
        """
        return "Trajectoire :\n" + str(self.array)

    def plot(self):
        """
        Plot a trajectory
        """
        fig = plt.figure('Trajectoire {0}'.format(self.type))
        fig.suptitle('Trajectoire {0}'.format(self.type))
        # 3d graph
        ax = fig.add_subplot(111, projection='3d')
        xdata = self.array[:, 0]
        ydata = self.array[:, 1]
        zdata = self.array[:, 2]
        ax.plot3D(xdata, ydata, zdata)
        ax.scatter3D(xdata, ydata, zdata)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        # Table
        # To do
        # fig.savefig('pics/trajectoire_{0}.png'.format(self.type))
        plt.show()