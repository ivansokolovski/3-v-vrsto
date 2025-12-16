/* 
 Narejeno po tutorialu + dodatek je bot ki igra optimalno
 brez alpha-beta pruninga ker je nepotreben za tako majhno igro
 algoritem in logika nista original, je pa bil program napisan
 ne copy-pastean.

 Ima par težav, ampak dokler se igra kot je bilo namenjeno igrat ni nobenih težav.
(npr. če vpišeš v vhod neko random sranje recimo nek character se bo lepo crashal program).
*/




#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>

char board[3][3];
const char PLAYER = 'X';
const char COMPUTER = 'O';

void resetBoard();
void printBoard();
bool areFreeSpaces();
void playerMove();
void computerMove(int);
int minimax(int, int);
char checkWinner();
void printWinner(char);

int main() {
    char wantToPlay;
    char winner = ' ';
    int move = 0;
    do {
        resetBoard();

        while(winner == ' ' && areFreeSpaces()) {
            printBoard();
            playerMove();
            winner = checkWinner();
            if(winner != ' ' || !areFreeSpaces()) {
                break;
            }
            computerMove(move);
            move++;
            winner = checkWinner();
            if(winner != ' ' || !areFreeSpaces()) {
                break;
            }
        }
        printBoard();
        printWinner(winner);
        
        do {
        printf("Ali zelite se igrati?: (D-da/N-ne): ");
        scanf(" %c", &wantToPlay);
        wantToPlay = toupper(wantToPlay);
        winner = ' ';
        }while(wantToPlay != 'D' && wantToPlay != 'N');

    } while (wantToPlay == 'D');

    printf("\n-------------------\nHVALA, DA SI SE POIGRAL/A!\n-------------------\n");
    
    return 0;
}
void resetBoard() {
    for (int i = 0; i < 3; i++) { // vrstice
        for (int j = 0; j < 3; j++) { // stolpci
            board[i][j] = ' ';
        }
    }
}
void printBoard() {
    printf(" %c | %c | %c \n", board[0][0], board[0][1], board[0][2]);
    printf("---|---|---\n");
    printf(" %c | %c | %c \n", board[1][0], board[1][1], board[1][2]);
    printf("---|---|---\n");
    printf(" %c | %c | %c \n", board[2][0], board[2][1], board[2][2]);
}
bool areFreeSpaces() {
    for (int i = 0; i < 3; i++) { // vrstice
        for (int j = 0; j < 3; j++) { // stolpci
            if (board[i][j] == ' ') {
                return true;
            }
        }
    }
    return false;
}
void playerMove() {
    int x;
    int y;
    do {
    printf("Vstavi stevilko stolpca(1-3): ");
    scanf(" %d", &y);
    printf("Vstavi stevilko vrstice(1-3): ");
    scanf(" %d", &x);
    x--;
    y--;

    if (board[x][y] != ' ') {
        printf("Neveljaven vnos.\n");
    }
    }while (board[x][y] != ' ');

    board[x][y] = PLAYER;
}
void computerMove(int move) {
    int bestScore = INT_MIN;
    int bestMove[2] = {-1, -1};

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == ' ') {
                board[i][j] = COMPUTER;
                int score = minimax(0, 0);
                board[i][j] = ' ';    
                if(score > bestScore) {
                    bestScore = score;
                    bestMove[0] = i;
                    bestMove[1] = j;
                }           
            }
        }
    }
    board[bestMove[0]][bestMove[1]] = COMPUTER;
} 

// algoritem za ugotavljanje optimalne poteze ki najhitreje privede do zmage.
int minimax(int depth, int isMaximizing) {

  // preverja rekurzivno - stalno bo prišel do konca ali je nekdo zmagal ali ni več prostih mest na plošči ali pa so
  // še vedno in se bo poklicala funkcija spet

    char result = checkWinner();
    if (result == COMPUTER) {
        // to se naredi da ugotovi optimalno najhitrejši način da zmaga
        return 10 - depth;
    }
    else if (result == PLAYER) {
        // prav tako to
        return depth - 10;
    }
    else if (!areFreeSpaces()) {
        return 0;
    }

    // obrača se med tem in !isMaximizing
    if(isMaximizing) {
        int bestScore = INT_MIN;
        for(int i = 0; i < 3; i++) {
            for(int j = 0; j < 3; j++) {
                if(board[i][j] == ' ') {
                    board[i][j] = COMPUTER;
                    int score = minimax(depth + 1, 0);
                    board[i][j] = ' ';
                    bestScore = (score > bestScore) ? score : bestScore;
                }
            }
        }
        return bestScore;

    }
    // tle je !isMaximizing
    else {
        int bestScore = INT_MAX;
        // preizkusimo vsa polja
        for(int i = 0; i < 3; i++) {
            for(int j = 0; j < 3; j++) {
                if(board[i][j] == ' ') {
                    board[i][j] = PLAYER;
                    // dobimo vrednost iz funkcije
                    // sprememba je v drugem argumentu (0 -> 1, 1 -> 0)
                    int score = minimax(depth + 1, 1);
                    board[i][j] = ' ';
                    // če je najboljši score ga posodobimo
                    bestScore = (score < bestScore) ? score : bestScore;
                }
            }
        }
        return bestScore;
    }
    
}

// preveri če je kdo zmagal igro (vse kombinacije zmagovalca)
char checkWinner() {
    for(int i = 0; i < 3; i++) {
        if(board[i][0] != ' ' && board[i][0] == board[i][1] && board[i][0] == board[i][2]) {
            return board[i][0];
        }
    }
    for(int i = 0; i < 3; i++) {
        if(board[0][i] != ' ' && board[0][i] == board[1][i] && board[0][i] == board[2][i]) {
            return board[0][i];
        }
    }
    if (board[0][0] != ' ' && board[0][0] == board[1][1] && board[0][0] == board[2][2]) {
        return board[0][0];
    }
    if (board[0][2] != ' ' && board[0][2] == board[1][1] && board[2][0] == board[0][2]) {
        return board[2][0];
    }
    return ' ';
    
}

// izpiše tistega, ki je zmagal (nikoli ti ker nisi dovolj dober :D ) -> zato tudi vedno 0 tock.
// lahko bi naredil, da je ena točka za izenačen izid, mogoče ko naredim GUI za to zadevo.
void printWinner(char winner) {
    if(winner == 'O') {
        printf("\n----------------\n");
        printf("IZGUBIL SI!\n");
        printf("TOCKE: 0\n");
        printf("----------------\n");
    }
    else {
        printf("\n----------------\n");
        printf("IZENACENO!\n");
        printf("TOCKE : 0\n");
        printf("----------------\n");
    }
}
