from fastapi import Fast


app = FastAPI()

@app.post("/alunos")
def criar_aluno(nome: str, email: str , db: Session = Depends(get_db)):
    aluno = Aluno(nome=nome, emai=email)
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno

@app.get("/alunos")
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).all


@app.post("/cursos")
def criar_curso(nome: str, email: str , db: Session = Depends(get_db)):
    curso = Curso(nome=nome, emai=email)
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso

@app.get("/cursos")
def listar_cursos(db: Session = Depends(get_db)):
    return db.query(Curso).all


@app.post("/incricoes")
def criar_incricao(aluno_id: int,curso_id:int,db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == curso_id).first()
    curso = db.query(Curso).filter(Curso.id == curso_id).first()

    if not aluno or not curso:
        raise HTTPException(status_code=404,detail "Aluno")
    

    inscricao = Inscricao(aluno_id = aluno_id,curso_id = curso)
    db.add(inscricao)
    db.commit()
    db.refresh(inscricao)
    return inscricao