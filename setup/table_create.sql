CREATE TABLE [dbo].[callcenter_summary] (
    [ID]                               INT            IDENTITY (1, 1) NOT NULL,
    [CustomerFirstName]                NVARCHAR (MAX) NULL,
    [CustomerLastName]                 NVARCHAR (MAX) NULL,
    [CustomerID]                       INT            NULL,
    [ConversationMainReason]           NVARCHAR (MAX) NULL,
    [CustomerSentiment]                NVARCHAR (MAX) NULL,
    [CommentOnAgentHandleConversation] NVARCHAR (MAX) NULL,
    [ConversationOutcome]              NVARCHAR (MAX) NULL,
    [ConversationSummary]              NVARCHAR (MAX) NULL,
    CONSTRAINT [PK_callcenter_summary] PRIMARY KEY CLUSTERED ([ID] ASC)
);