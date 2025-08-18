from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2, database

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db),
         current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="此貼文並不存在!")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    
    if vote.dir == 1:  # 使用者要投票
        if found_vote: # 已經投過了
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="已經投過囉~")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"訊息": "投票成功!"}
    else:  # 取消投票
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="您尚未投過票喔!")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"訊息": "已成功取消投票!"}