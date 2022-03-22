// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    //using SafeMathChainlink for uint256; // solo per solidity < 0.8.8

    mapping(address => uint256) public address_amount;
    AggregatorV3Interface public priceFeed;

    address[] private founders;
    address private owner;
    uint256 private constant MINIMUM_USD = 50;

    constructor(address _priceFeed) public {
        //eseguito al momento del deploy e poi mai più
        owner = msg.sender; // il mio address
        priceFeed = AggregatorV3Interface(_priceFeed); // ABI e address
    }

    function fund() public payable {
        uint256 minimumUsd = MINIMUM_USD * 10**18;

        // una sorta di assert, se fallisce fa revert a restituisce tutto, anche il gas che non è stato speso!
        require(
            getConversionRate(msg.value) >= minimumUsd,
            "You need to spend at least 50$ of ETH"
        );

        address_amount[msg.sender] += msg.value;
        founders.push(msg.sender);
        // ETH -> USD? dobbiamo ottenerlo da un Oracle (contracts non vedono il mondo esterno)
        // ciò perché i contracts devono dare lo stesso output su tutti i nodi (ridondanza di comportamento) -> determinismo
        // Una chiamata API può dare risposte diverse ai nodi in base a parametri estrerni (eg tempo della richiesta)
    }

    // ritorna il minimo numero di ETH che occorre pagare per accettare la transazione
    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUsd = MINIMUM_USD * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18; // serve per non fare errotondamenti durante la divisione successiva
        return (minimumUsd * precision) / price;
    }

    // i modificatori permettono di eseguire codice (eg require) prima o dopo la chiamata della funzione decorata
    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Only the owner of the contract can call this function."
        );
        _; // dopodiché, esegui il resto del codice
    }

    function withdraw() public payable onlyOwner {
        //solo l'owner del contratto può fare withdraw
        //require(msg.sender == owner, "Only the owner of the contract can call this function.");

        // sender.transfer(mny) trasferisce mny all'indirizzo di sender. mny deve essere un balance
        // this si riferisce al contract attuale
        // balance di un address restituisce il totale di ETH di un dato address
        // payable dichiara che l'address può ricevere token.
        payable(msg.sender).transfer(address(this).balance);
        // come capisco di resettare l'address corretto?
        // mi salvo tutti quelli che hanno mandato fondi e resetto tutti i loro contributi (basterebbe buttare via tutto se voglio dimenticare i founder)
        for (uint256 i = 0; i < founders.length; i++) {
            address_amount[founders[i]] = 0;
        }

        founders = new address[](0); // reset
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        // chiamata all'oracolo
        (
            ,
            //uint80 roundId
            int256 answer, //uint256 startedAt //uint256 updatedAt //uint80 answeredInRound
            ,
            ,

        ) = priceFeed.latestRoundData();
        return uint256(answer * (10**10));
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 10**18;
        return ethAmountInUsd;
    }
}
