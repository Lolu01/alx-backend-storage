-- creates a stored procedure ComputeAverageScoreForUser that computes and stores the average score for a student.
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    UPDATE users 
    SET average_score = (
        SELECT SUM(score) / COUNT(score) 
        FROM corrections 
        WHERE corrections.user_id = user_id
    ) 
    WHERE id = user_id; 
END;

//

DELIMITER ;
