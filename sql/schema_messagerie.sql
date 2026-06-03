--
-- Create model Conversation
--
CREATE TABLE `conversations` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `date_creation` datetime(6) NOT NULL, `matching_id` bigint NULL, `utilisateur1_id` bigint NOT NULL, `utilisateur2_id` bigint NOT NULL);
--
-- Create model Message
--
CREATE TABLE `messages` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `contenu` longtext NOT NULL, `lu` bool NOT NULL, `date_envoi` datetime(6) NOT NULL, `conversation_id` bigint NOT NULL, `expediteur_id` bigint NOT NULL);
ALTER TABLE `conversations` ADD CONSTRAINT `conversations_utilisateur1_id_utilisateur2_id_681ebf3a_uniq` UNIQUE (`utilisateur1_id`, `utilisateur2_id`);
ALTER TABLE `conversations` ADD CONSTRAINT `conversations_matching_id_0071fa86_fk_match_suggestions_id` FOREIGN KEY (`matching_id`) REFERENCES `match_suggestions` (`id`);
ALTER TABLE `conversations` ADD CONSTRAINT `conversations_utilisateur1_id_9570320e_fk_users_id` FOREIGN KEY (`utilisateur1_id`) REFERENCES `users` (`id`);
ALTER TABLE `conversations` ADD CONSTRAINT `conversations_utilisateur2_id_23bdea64_fk_users_id` FOREIGN KEY (`utilisateur2_id`) REFERENCES `users` (`id`);
ALTER TABLE `messages` ADD CONSTRAINT `messages_conversation_id_5ef638db_fk_conversations_id` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`);
ALTER TABLE `messages` ADD CONSTRAINT `messages_expediteur_id_da0517a8_fk_users_id` FOREIGN KEY (`expediteur_id`) REFERENCES `users` (`id`);
