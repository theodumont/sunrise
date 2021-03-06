# coding: utf8

import math
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import modules.utils as utils


# PARAMETERS

class Parameters(object):

    def __init__(self):
        """
        Parameters class constructor.
        """
        # Hangar
        self.hangar_x = 125     # cm
        self.hangar_y = 125
        self.hangar_z = 100
        self.dimensions_hangar = np.array([self.hangar_x,
                                           self.hangar_y,
                                           self.hangar_z])
        # Mobile
        self.mobile_x = 25      # cm
        self.mobile_y = 25
        self.mobile_z = 30
        self.dimensions_mobile = np.array([self.mobile_x,
                                           self.mobile_y,
                                           self.mobile_z])
        # maximal steps authorized
        self.max_step_x = 1     # cm
        self.max_step_y = 1
        self.max_step_z = 1
        self.max_step_alpha = math.radians(10)
        self.max_step_beta = math.radians(10)
        self.max_step_gamma = math.radians(10)
        # array
        self.max_step = np.array([self.max_step_x, self.max_step_y,
                                  self.max_step_z, self.max_step_alpha,
                                  self.max_step_beta, self.max_step_gamma])
        # drummotor diameter
        self.drum_motor_diameter = .9       # cm
        # display
        self.display = False
        self.dim6d = ['x', 'y', 'z', 'alpha', 'beta', 'gamma']
        self.typedim = ['translation', 'rotation']
        self.units = ['cm', 'rad']


    def __str__(self):
        """
        Display the parameters.
        """
        self.display_step()
        self.display_motors()
        self.display_hangar()
        self.display_mobile()
        return ""


    def display_step(self):
        """Display step parameters."""
        print("\nSteps:")
        for dim in range(6):
            print("{}-{} step: {:.3f} {}".format(self.dim6d[dim],
                                                 self.typedim[dim//3],
                                                 self.max_step[dim],
                                                 self.units[dim//3]))

    def display_motors(self):
        """Display motors parameters."""
        print(f"\nDrummotor diameter: {self.drum_motor_diameter} cm")

    def display_hangar(self):
        """Display hangar parameters."""
        print("\nHangar:")
        for dim in range(3):
            print(f"{self.dim6d[dim]}: {self.dimensions_hangar[dim]:.3f} m")

    def display_mobile(self):
        """Display mobile parameters."""
        print("\nMobile:")
        for dim in range(3):
            print(f"{self.dim6d[dim]}: {self.dimensions_mobile[dim]:.3f} m")


# 3D OBJECTS

class Object3d(object):

    def __init__(self, name, parameters, *args, **kwargs):
        """
        Object3d class constructor.
        """
        super().__init__(*args, **kwargs)
        self._name = name
        self._position = np.array([0, 0, 0, 0, 0, 0])
        # self._dimensions = dimensions

    def __str__(self):
        """
        Prettily display an Object3d.
        """
        str_dim = f"| > Dimensions: {self.dimensions}\n"
        str_pos = f"| > Position: {self.position[0:3]}\n|             {self.position[3:6]}\n"
        str_vertices = "| > Vertices:\n"
        for vertex in self.vertices:
            str_vertices += '|   '
            str_vertices += str(vertex) + '\n'
        return f"\n| {self.name}:\n{str_dim}{str_pos}{str_vertices}"

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, destination):
        """
        Move a mobile.
        """
        # change position
        self._position = destination
        # refresh the vertices
        self.vertices = utils.pos_to_vertices(self.position, self.dimensions)
        print(f"{self.name} has moved!")

    @property
    def name(self):
        return self._name


class Mobile(Object3d):

    def __init__(self, parameters, *args, **kwargs):
        """
        Mobile class constructor.
        """
        super().__init__("Mobile", parameters, *args, **kwargs)
        self._dimensions = parameters.dimensions_mobile
        self.vertices = utils.pos_to_vertices(self.position, self.dimensions)

    @property
    def dimensions(self):
        return self._dimensions


class Hangar(Object3d):

    def __init__(self, parameters, *args, **kwargs):
        """
        Hangar class constructor.
        """
        super().__init__("Hangar", parameters, *args, **kwargs)
        self._dimensions = parameters.dimensions_hangar
        self.vertices = utils.pos_to_vertices(self.position, self.dimensions)

    @property
    def dimensions(self):
        return self._dimensions


# TRAJECTORY

class Trajectory(object):

    def __init__(self, parameters, initial_traj, *args, **kwargs):
        """
        Trajectory class constructor.

        to do: describe attributes
        """
        super().__init__(*args, **kwargs)
        self.parameters = parameters
        # initial trajectory
        self.initial_traj = initial_traj
        # discretized trajectory
        self.discretized_traj_pos,\
        self.discretized_traj_var = self.get_discretized()
        # cables
        self.cable_length,\
        self.cable_var = self.get_length()
        # motor rotations
        self.motor_rotation,\
        self.motor_var = self.get_rotation()

    def __str__(self):
        """
        Prettily display a trajectory
        """
        display = (
            f"Initial trajectory:\n{self.initial_traj}\n"
            f"Discretized trajectory:\n{self.discretized_traj_pos}\n"
            f"Cable lengths:\n{self.cable_length}\n"
            f"Cable var:\n{self.cable_var}\n"
            f"Motor rotations:\n{self.motor_rotation}\n"
        )
        return display

    def get_discretized(self):
        """
        Discretize a trajectory
        """
        return utils.discretize_traj(self.initial_traj,
                                     self.parameters.max_step)

    def get_length(self):
        """
        Transform a discretized trajectory into the motor cable lengths
        """
        return utils.disc_to_length(self.discretized_traj_pos,
                                    self.parameters.dimensions_mobile,
                                    self.parameters.dimensions_hangar)

    def get_rotation(self):
        """
        Transform the motor cable lengths into the motor rotations
        """
        return utils.length_to_rotation(self.cable_var,
                                        self.parameters.drum_motor_diameter)

    def animate(self, save):
        """
        Animate a trajectory

        To add:
        - parameters of the movement?
        """
        print("Animating...")

        # SETUP
        fig = plt.figure(num="Trajectory animation", figsize=(10,6))
        animated_list = []
        # Content of animated_list:
        # 1. 3D trajectory, [0];
        # 2. cable lengths, [1:9].
        # 3. motor rotations, [9:17].

        # TRAJECTORY
        ax_traj = fig.add_subplot(121, projection='3d')
        ax_traj.set_title("3D trajectory")
        ax_traj.set_xlabel("x (cm)")
        ax_traj.set_ylabel("y (cm)")
        ax_traj.set_zlabel("z (cm)")
        xlim_traj = self.parameters.dimensions_hangar[0] / 2
        ylim_traj = self.parameters.dimensions_hangar[1] / 2
        zlim_traj = self.parameters.dimensions_hangar[2] / 2
        ax_traj.set_xlim3d((-xlim_traj, xlim_traj))
        ax_traj.set_ylim3d((-ylim_traj, ylim_traj))
        ax_traj.set_zlim3d((-zlim_traj, zlim_traj))
        trajectory, = ax_traj.plot([], [], [], marker='')
        animated_list.append(trajectory)

        # CABLES
        ax_cable_len = fig.add_subplot(222)
        ax_cable_len.set_title("Cable lengths")
        ax_cable_len.set_xlabel("time (dt)")
        ax_cable_len.set_ylabel("cable length (cm)")
        plt.xlim((0, 1.5 * len(self.cable_length)))
        plt.ylim((.9 * np.min(self.cable_length), 1.1 * np.max(self.cable_length)))
        for cable_nb in range(8):
            cable, = ax_cable_len.plot([], [], label=f"cable {cable_nb}")
            animated_list.append(cable)
        plt.legend()

        # MOTOR ROTATIONS
        ax_rot = fig.add_subplot(224)
        ax_rot.set_title(f"Motor rotations")
        ax_rot.set_xlabel("time (dt)")
        ax_rot.set_ylabel("motor rotation (rad)")
        plt.xlim((0, 1.5 * len(self.motor_rotation)))
        plt.ylim((1.3 * np.min(self.motor_rotation), 1.3 * np.max(self.motor_rotation)))
        for motor_nb in range(8):
            motor, = ax_rot.plot([], [], label=f"motor {motor_nb}")
            animated_list.append(motor)
        plt.legend()

        # SETUP
        plt.tight_layout()

        def update_fig(i):
            """
            Animation function
            """
            # trajectory update
            animated_list[0].set_data(self.discretized_traj_pos[0:i+1, 0],
                                      self.discretized_traj_pos[0:i+1, 1])
            animated_list[0].set_3d_properties(self.discretized_traj_pos[0:i+1, 2])
            # cables update
            for cable_nb in range(8):
                animated_list[1 + cable_nb].set_data(
                        range(i+1),
                        self.cable_length[0:i+1, cable_nb])
            # motors update
            for motor_nb in range(8):
                animated_list[1 + 8 + motor_nb].set_data(
                        range(i+1),
                        self.motor_rotation[0:i+1, motor_nb])
            return animated_list

        anim = animation.FuncAnimation(fig, update_fig,
                                       frames=len(self.discretized_traj_pos),
                                       interval=10,
                                       blit=True)
        # save and show
        if save:
            print("Saving gif...")
            anim.save('animation.gif', fps=30)
        plt.show()
