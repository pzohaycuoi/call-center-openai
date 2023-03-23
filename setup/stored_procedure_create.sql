CREATE PROCEDURE callcenter_insert_summary_data
    @CustomerFirstName NVARCHAR,
    @CustomerLastName NVARCHAR,
    @CustomerID INT,
    @ConversationMainReason NVARCHAR,
    @CustomerSentiment NVARCHAR,
    @CommentOnAgentHandleConversation NVARCHAR,
    @ConversationOutcome NVARCHAR,
    @ConversationSummary NVARCHAR
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO dbo.callcenter_summary (
        CustomerFirstName, 
        CustomerLastName, 
        CustomerID,
        ConversationMainReason,
        CustomerSentiment,
        CommentOnAgentHandleConversation,
        ConversationOutcome,
        ConversationSummary
    )
    VALUES (
        @CustomerFirstName,
        @CustomerLastName,
        @CustomerID,
        @ConversationMainReason,
        @CustomerSentiment,
        @CommentOnAgentHandleConversation,
        @ConversationOutcome,
        @ConversationSummary
    );
END