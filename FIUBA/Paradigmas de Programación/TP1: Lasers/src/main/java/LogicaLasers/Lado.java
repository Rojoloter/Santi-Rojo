package LogicaLasers;

import java.util.List;

public interface Lado {
    List<Laser> interactuarLaser(int direccionVertical, int direccionHorizontal);
    void setObjetivo(Objetivo obj);
}

