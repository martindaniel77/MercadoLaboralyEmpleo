from database import db

class DimTiempo(db.Model):
    __tablename__ = 'dim_tiempo'

    id_tiempo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    anio = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    trimestre = db.Column(db.String(10), nullable=False)
    fecha_registro = db.Column(db.Date, nullable=False)

    # Relación inversa con la tabla de hechos
    hechos = db.relationship('FactGigEconomy', backref='tiempo', lazy=True)


class DimGeografia(db.Model):
    __tablename__ = 'dim_geografia'

    id_geografia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nivel_territorial = db.Column(db.String(50), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    codigo_iso_pais = db.Column(db.String(10), nullable=False)
    departamento_region = db.Column(db.String(100), nullable=False)
    ciudad_municipio = db.Column(db.String(100), nullable=False)

    # Relación inversa con la tabla de hechos
    hechos = db.relationship('FactGigEconomy', backref='geografia', lazy=True)


class DimPlataforma(db.Model):
    __tablename__ = 'dim_plataforma'

    id_plataforma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_plataforma = db.Column(db.String(100), nullable=False)
    categoria_servicio = db.Column(db.String(100), nullable=False)
    plataforma_principal = db.Column(db.String(100), nullable=False)

    # Relación inversa con la tabla de hechos
    hechos = db.relationship('FactGigEconomy', backref='plataforma', lazy=True)


class DimTrabajador(db.Model):
    __tablename__ = 'dim_trabajador'

    id_trabajador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_registro = db.Column(db.String(50), unique=True, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    nivel_educativo = db.Column(db.String(100), nullable=False)
    antiguedad_meses = db.Column(db.Integer, nullable=False)
    dependencia_ingresos = db.Column(db.String(100), nullable=False)
    afiliacion_salud = db.Column(db.String(100), nullable=False)
    afiliacion_pension = db.Column(db.String(100), nullable=False)
    cuenta_con_arl = db.Column(db.String(100), nullable=False)
    fuente_origen_id = db.Column(db.String(50), nullable=False)

    # Relación inversa con la tabla de hechos
    hechos = db.relationship('FactGigEconomy', backref='trabajador', lazy=True)


class FactGigEconomy(db.Model):
    __tablename__ = 'fact_gig_economy'

    id_hecho = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Claves Foráneas (Foreign Keys)
    id_tiempo = db.Column(db.Integer, db.ForeignKey('dim_tiempo.id_tiempo'), nullable=False)
    id_geografia = db.Column(db.Integer, db.ForeignKey('dim_geografia.id_geografia'), nullable=False)
    id_plataforma = db.Column(db.Integer, db.ForeignKey('dim_plataforma.id_plataforma'), nullable=False)
    id_trabajador = db.Column(db.Integer, db.ForeignKey('dim_trabajador.id_trabajador'), nullable=False)

    # Medidas cuantitativas del modelo
    ingreso_bruto_mensual_cop = db.Column(db.Numeric(12, 2), nullable=False)
    costos_operativos_mensuales_cop = db.Column(db.Numeric(12, 2), nullable=False)
    ingreso_neto_mensual_cop = db.Column(db.Numeric(12, 2), nullable=False)
    ingreso_neto_hora_usd = db.Column(db.Numeric(10, 2), nullable=False)
    horas_semanales = db.Column(db.Numeric(5, 2), nullable=False)
    calificacion_promedio_app = db.Column(db.Numeric(3, 2), nullable=False)